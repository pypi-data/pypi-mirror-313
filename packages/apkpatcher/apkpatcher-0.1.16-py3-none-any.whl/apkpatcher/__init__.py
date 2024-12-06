#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import shutil
import tempfile
import subprocess
import logging
import re
from pathlib import Path
import pyaxml

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree


def new_logger(level: "logging._Level") -> logging.Logger:
    logger = logging.getLogger("apkpatcher")

    class CustomFormatter(logging.Formatter):

        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        tmp_format = "%(asctime)s - %(name)s [ %(levelname)s ] - %(message)s (%(filename)s:%(lineno)d)"

        FORMATS = {
            logging.DEBUG: grey + tmp_format + reset,
            logging.INFO: grey + tmp_format + reset,
            logging.WARNING: yellow + tmp_format + reset,
            logging.ERROR: red + tmp_format + reset,
            logging.CRITICAL: bold_red + tmp_format + reset,
        }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)

    ch = logging.StreamHandler()
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    logger.setLevel(level)
    return logger


def plba(filename: str | Path, arch):
    p = Path(filename)
    return f"{p.parent}/{p.stem}_{arch}.so"


class Patcher:

    ARCH_ARM = "arm"
    ARCH_ARM64 = "arm64"
    ARCH_X86 = "x86"
    ARCH_X64 = "x64"
    ARCH_X86_64 = "x86_64"

    DEFAULT_GADGET_NAME = "libfrida-gadget.so"
    DEFAULT_HOOKFILE_NAME = "libhook.js.so"
    DEFAULT_CONFIG_NAME = "generatedConfigFile.config"

    CONFIG_BIT = 1 << 0
    AUTOLOAD_BIT = 1 << 1

    INTERNET_PERMISSION = "android.permission.INTERNET"

    def __init__(
        self,
        apk: str | Path,
        sdktools: str | Path,
        version: str,
        logger: logging.Logger | None = None,
    ):
        """
        Initialisation of patcher

        Parameters:
                    apk (str): path of the apk
                    sdktools (str): path of the sdktools for zipalign
                    version (str): version to choose the correct path of
                    logger (logging.Logger) logger

        """
        self.apk: Path = Path(apk)
        self.arch: str | None = None
        self.sdktools: Path = Path(sdktools)
        self.version: str = version
        self.final_dir: Path = Path("")
        self._pause: bool = False
        self.plugin: Path | None = None
        self.entrypoint_smali_path: Path | None = None
        self.entrypoint_class: str | None = None
        self.path_build_tools = Path(
            f"{sdktools}/build-tools/{version}/" if (sdktools and version) else ""
        )
        self.network_certificates: list[Path] = []
        if logger is None:
            self.logger : logging.Logger = new_logger(logging.INFO)
        else:
            self.logger : logging.Logger = logger

    def check_binaries_tools_installed(self):
        binaries = ["apksigner", "zipalign"]
        for b in binaries:
            file = Path(f"{self.path_build_tools}/{b}")
            if not file.is_file():
                self.logger.error("Couldn't find %s", b)
                self.logger.error(
                    "it should be installed on your build tools here %s", self.path_build_tools
                )
                return -1
        try:
            subprocess.check_output("apktool", shell=True)
        except subprocess.CalledProcessError:
            self.logger.error("Couldn't find apktool")
        return 1

    ################################################################################
    #                                                                              #
    #            CERTIFICATES                                                      #
    #                                                                              #
    ################################################################################

    def add_network_certificate(self, cert: Path):
        self.network_certificates.append(cert)

    def inject_custom_network_certificate(self, rsc, path_network: str):
        netsec_path = self.final_dir / path_network
        ca_path = self.final_dir / "res/my_ca"

        _id = rsc.add_id_public(
            rsc.get_packages()[0], "raw", "network_security_config_ca", "res/my_ca"
        )

        buf = f"""
        <network-security-config>
            <base-config cleartextTrafficPermitted="true">
                <trust-anchors>
                    <certificates src="system"/>
                    <certificates src="user"/>
                    <certificates src="@{hex(_id)[2:]}"/>
                </trust-anchors>
            </base-config>
        </network-security-config>
        """

        root = etree.fromstring(buf)
        res_aml = pyaxml.axml.AXML()
        res_aml.from_xml(root)
        with open(netsec_path, "wb") as f:
            f.write(res_aml.pack())

        for cert in self.network_certificates:
            shutil.copyfile(cert, ca_path)
        self.logger.info("Custom certificate was injected inside the apk")

    def create_security_config_xml(self, path_network: str):
        """Create security config file for add certificate

        Args:
            path_network (str): path network
        """
        netsec_path = self.final_dir / path_network

        buf = """
        <network-security-config>
            <base-config cleartextTrafficPermitted="true">
                <trust-anchors>
                    <certificates src="system"/>
                    <certificates src="user"/>
                </trust-anchors>
            </base-config>
        </network-security-config>
        """
        root = etree.fromstring(buf)
        res_aml = pyaxml.axml.AXML()
        res_aml.from_xml(root)
        with open(netsec_path, "wb") as f:
            f.write(res_aml.pack())

        self.logger.info("The network_security_config.xml file was created!")

    def enable_user_certificates(self, rsc: pyaxml.ARSC):
        """Enable user certificate

        Args:
            rsc (pyaxml.ARSC): return ARSC file
        """
        path_network = self.inject_user_certificates_label(rsc)
        if path_network:
            if self.network_certificates:
                self.inject_custom_network_certificate(rsc, path_network)
            else:
                self.create_security_config_xml(path_network)

    def inject_user_certificates_label(self, rsc: pyaxml.ARSC) -> str:
        """Inject a proxy certificate directly inside the application

        Args:
            rsc (pyaxml.ARSC): ARSC file (resource file of Android)

        Raises:
            FileNotFoundError: raise when manifest is not found

        Returns:
            str: return the path of network file
        """
        self.logger.info("Injecting Network Security label to accept user certificates...")

        manifest_path = self.final_dir / "AndroidManifest.xml"

        if not manifest_path.is_file():
            self.logger.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            raise FileNotFoundError("manifest not found")

        with open(manifest_path, "rb") as fp:
            buf = fp.read()

            _id = rsc.get_id_public(rsc.get_packages()[0], "xml", "network_security_config")
            if not _id:
                path_network: str = "res/network_security_config.xml"
                _id = rsc.add_id_public(
                    rsc.get_packages()[0],
                    "xml",
                    "network_security_config",
                    path_network,
                )
            else:
                _id, path_network = _id
                path_network = pyaxml.StringBlocks(proto=rsc.proto.stringblocks).decode_str(
                    path_network
                )

            axml, _ = pyaxml.AXML.from_axml(buf)
            xml = axml.to_xml()
            application = xml.findall("./application")[0]
            application.attrib[
                "{http://schemas.android.com/apk/res/android}networkSecurityConfig"
            ] = f"@{hex(_id)[2:]}"
            res_aml = pyaxml.axml.AXML()
            res_aml.from_xml(xml)

            with open(manifest_path, "wb") as fp_out:
                fp_out.write(res_aml.pack())

            self.logger.info("The Network Security label was added!")

        return path_network

    ################################################################################
    #                                                                              #
    #                        PERMISSIONS                                           #
    #                                                                              #
    ################################################################################

    def has_permission(self, permission_name: str) -> bool:
        """
        Check if the apk have 'permission_name' as permission

        Parameters:
                    permission_name (str): name of the permission with format:
                    android.permission.XXX

        Returns:
                has_permission (bool): permission is present
        """
        manifest_path = self.final_dir / "AndroidManifest.xml"

        if not manifest_path.is_file():
            self.logger.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            raise FileNotFoundError("manifest not found")

        with open(manifest_path, "rb") as f:
            # Read AXML and get XML object
            axml, _ = pyaxml.AXML.from_axml(f.read())
            xml = axml.to_xml()

            # Search over all the application permissions
            android_name = "{http://schemas.android.com/apk/res/android}name"
            for permission in xml.findall("./uses-permission"):
                if permission.attrib[android_name] == permission_name:
                    self.logger.info(
                        "The app %s has the permission '%s'", self.apk, permission_name
                    )
                    return True

        self.logger.info("The app %s doesn't have the permission '%s'", self.apk, permission_name)
        return False

    def inject_permission_manifest(self, permission: str):
        """
        Inject permission on the Manifest
        """
        self.logger.info("Injecting permission %s in Manifest...", permission)

        manifest_path = self.final_dir / "AndroidManifest.xml"

        if not manifest_path.is_file():
            self.logger.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            return False

        with open(manifest_path, "rb") as fp:
            buf = fp.read()

            axml, _ = pyaxml.AXML.from_axml(buf)
            xml = axml.to_xml()
            res_aml: pyaxml.AXML | None = None
            for i, elt in enumerate(xml):  # range(len(xml)):
                if elt.tag in ("application", "uses-permission"):
                    newperm = etree.Element("uses-permission")
                    newperm.attrib["{http://schemas.android.com/apk/res/android}name"] = permission
                    xml.insert(i, newperm)
                    res_aml = pyaxml.axml.AXML()
                    res_aml.from_xml(xml)
                    break
        if res_aml is None:
            self.logger.error("resource file could not be found")
            return False
        with open(manifest_path, "wb") as fp:
            fp.write(res_aml.pack())
        return True

    ################################################################################
    #                                                                              #
    #                EXTRACT REPACK APK                                            #
    #                                                                              #
    ################################################################################

    def extract_apk(self):
        """
        Extract the apk on the temporary folder
        """

        self.logger.info("Extracting %s (without resources) to %s", self.apk, self.final_dir)
        # result = subprocess.check_output(
        #    " ".join(["unzip", "-d", self.final_dir.absolute().as_posix(), self.apk.absolute().as_posix()]), shell=True
        # )
        result = subprocess.check_output(
            " ".join(
                [
                    "apktool",
                    "-f",
                    "-r",
                    "d",
                    "-o",
                    self.final_dir.absolute().as_posix(),
                    self.apk.absolute().as_posix(),
                ]
            ),
            shell=True,
        )
        print(result.decode("utf-8"))

    def sign_and_zipalign(self, apk_path: Path, splits_apk):
        """
        sign and zipalign file
        """

        self.logger.info("Optimizing with zipalign...")

        tmp_target_file: Path = apk_path.rename(
            apk_path.with_name(apk_path.stem.replace(".apk", "_tmp.apk"))
        )

        subprocess.call(
            f"{self.path_build_tools}/zipalign -p 4 {tmp_target_file} {apk_path}",
            stderr=subprocess.STDOUT,
            shell=True,
        )

        tmp_target_file.unlink()

        self.logger.info("Generating a random key...")
        subprocess.call(
            "keytool -genkey -keyalg RSA -keysize 2048 -validity 700 -noprompt -alias apkpatcheralias1 -dname "
            '"CN=apk.patcher.com, OU=ID, O=APK, L=Patcher, S=Patch, C=BR" -keystore apkpatcherkeystore '
            "-storepass password -keypass password 2> /dev/null",
            shell=True,
        )

        self.logger.info("Signing the patched apk...")
        subprocess.call(
            f"{self.path_build_tools}/apksigner sign --ks apkpatcherkeystore"
            f" --ks-key-alias apkpatcheralias1 --key-pass pass:password "
            f"--ks-pass pass:password --out {apk_path} {apk_path}",
            shell=True,
        )

        for split in splits_apk:
            split_new_name = split.replace(".apk", "_new_signed.apk")
            subprocess.call(
                f"{self.path_build_tools}apksigner sign --ks apkpatcherkeystore"
                f" --ks-key-alias apkpatcheralias1 --key-pass pass:password "
                f"--ks-pass pass:password --out {split_new_name} {split}",
                shell=True,
            )

        Path("apkpatcherkeystore").unlink()

        self.logger.info("The apk was signed!")

        self.logger.info("The file was optimized!")

    def pause(self, pause: bool) -> None:
        """enable a pause during the process to edit the application

        Args:
            pause (bool): pause parameter
        """
        self._pause = pause

    def set_plugin(self, plugin: str | Path) -> None:
        """set a plugin

        Args:
            plugin (str | Path): _description_
        """
        self.plugin = Path(plugin)

    def repackage_apk(self, target_file: Path | None = None):
        """
        repackage the apk

        Parameters:
                    - target_file (str) : the path of the new apk created if
                      none, a new apk will be created with suffix "_patched.apk"
        """
        if self.plugin:
            subprocess.run([self.plugin, self.final_dir], check=True)
        if self._pause:
            print(f"You can modify the apk here: {self.final_dir}")
            input()
        if target_file is None:
            target_file = self.apk.with_name(self.apk.stem + "_patched.apk")

            if target_file.is_file():
                timestamp = str(time.time()).replace(".", "")
                new_file_name = target_file.with_name(f"{target_file.stem}_{timestamp}.apk")
                target_file = new_file_name

        self.logger.info("Repackaging apk to %s", target_file)
        self.logger.info("This may take some time...")

        subprocess.check_output(
            " ".join(
                [
                    "apktool",
                    "--use-aapt2",
                    "b",
                    "-o",
                    target_file.as_posix(),
                    self.final_dir.as_posix(),
                ]
            ),
            shell=True,
        )

        return target_file

    ################################################################################
    #                                                                              #
    #                INJECT NATIVE CODE                                            #
    #                                                                              #
    ################################################################################

    def get_entrypoint_class_name(self) -> str | None:
        """
        get the class name of the entrypoint
        """
        entrypoint_class = None
        manifest_path = self.final_dir / "AndroidManifest.xml"

        if not manifest_path.is_file():
            self.logger.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            raise FileNotFoundError("manifest not found")

        with open(manifest_path, "rb") as f:
            # Read AXML and get XML object
            axml, _ = pyaxml.AXML.from_axml(f.read())
            xml = axml.to_xml()
            # Look over all the activities and try to find either one with MAIN as action
            android_name = "{http://schemas.android.com/apk/res/android}name"
            for activity in xml.findall("./application/activity"):
                for action in activity.findall("intent-filter/action"):
                    if action.attrib[android_name] == "android.intent.action.MAIN":
                        entrypoint_class = activity.attrib[android_name]
                        break

            # Do the same for activities alias in case we did not find the main activity
            if not entrypoint_class:
                android_target_activity = (
                    "{http://schemas.android.com/apk/res/android}targetActivity"
                )
                for alias in xml.findall("./application/activity-alias"):
                    for action in alias.findall("intent-filter/action"):
                        if action.attrib[android_name] == "android.intent.action.MAIN":
                            entrypoint_class = alias.attrib[android_target_activity]
                            break

            # Check if entry point is relative, if so search in the Manifest package
            if entrypoint_class is None:
                self.logger.error("Fail to find entrypoint class")
                return entrypoint_class
            if entrypoint_class.startswith("."):
                entrypoint_class = xml.attrib["package"] + entrypoint_class

        if entrypoint_class is None:
            self.logger.error("Fail to find entrypoint class")

        return entrypoint_class

    def get_entrypoint_smali_path(self) -> Path | None:
        """
        get the path of apk entrypoint on the smali files
        """
        entrypoint_final_path = None
        if self.entrypoint_class is None:
            raise ValueError("entrypoint class is None")

        for file in self.final_dir.iterdir():
            if file.name.startswith("smali"):
                entrypoint_tmp = (
                    self.final_dir / file / (self.entrypoint_class.replace(".", "/") + ".smali")
                )
                if entrypoint_tmp.is_file():
                    entrypoint_final_path = entrypoint_tmp
                    break

        if entrypoint_final_path is None:
            self.logger.error("Couldn't find the application entrypoint")
            sys.exit(1)
        else:
            self.logger.info("Found application entrypoint at %s", entrypoint_final_path)

        return entrypoint_final_path

    def insert_frida_loader(self, frida_lib_name="frida-gadget"):
        """
        inject snippet to load frida-gadget in smali code
        """
        partial_injection_code = """
    const-string v0, "<LIBFRIDA>"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

        """.replace(
            "<LIBFRIDA>", frida_lib_name
        )

        full_injection_code = """
.method static constructor <clinit>()V
    .locals 1

    .prologue
    const-string v0, "<LIBFRIDA>"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    return-void
.end method
        """.replace(
            "<LIBFRIDA>", frida_lib_name
        )

        with open(self.entrypoint_smali_path, "r", encoding="ascii") as smali_file:
            content = smali_file.read()

            if frida_lib_name in content:
                self.logger.info("The frida-gadget is already in the entrypoint. Skipping...")
                return False

            direct_methods_start_index = content.find("# direct methods")
            direct_methods_end_index = content.find("# virtual methods")

            if direct_methods_start_index == -1 and direct_methods_end_index == -1:
                self.logger.error("Could not find direct methods.")
                return False

            class_constructor_start_index = content.find(
                ".method static constructor <clinit>()V",
                direct_methods_start_index,
                direct_methods_end_index,
            )

            if class_constructor_start_index == -1:
                has_class_constructor = False
            else:
                has_class_constructor = True

            class_constructor_end_index = -1
            if has_class_constructor:
                class_constructor_end_index = content.find(
                    ".end method",
                    class_constructor_start_index,
                    direct_methods_end_index,
                )

                if has_class_constructor and class_constructor_end_index == -1:
                    self.logger.error("Could not find the end of class constructor.")
                    return False

            prologue_start_index = -1
            if has_class_constructor:
                prologue_start_index = content.find(
                    ".prologue",
                    class_constructor_start_index,
                    class_constructor_end_index,
                )

            no_prologue_case = False
            locals_start_index = -1
            if has_class_constructor and prologue_start_index == -1:
                no_prologue_case = True

                locals_start_index = content.find(
                    ".locals ",
                    class_constructor_start_index,
                    class_constructor_end_index,
                )

                if no_prologue_case and locals_start_index == -1:
                    self.logger.error(
                        'Has class constructor. No prologue case, but no "locals 0" found.'
                    )
                    return False

            locals_end_index = -1
            if no_prologue_case:
                locals_end_index = locals_start_index + len("locals ")  # X')
                x = re.search(r"^ *\d+", content[locals_end_index + 1 :])
                locals_end_index += x.span()[1]

            prologue_end_index = -1
            if has_class_constructor and prologue_start_index > -1:
                prologue_end_index = prologue_start_index + len(".prologue") + 1

            if has_class_constructor:
                if no_prologue_case:
                    new_content = content[0:locals_end_index]

                    if content[locals_end_index] == "0":
                        new_content += "1"
                    else:
                        new_content += content[locals_end_index]

                    new_content += "\n\n    .prologue"
                    new_content += partial_injection_code
                    new_content += content[locals_end_index + 1 :]
                else:
                    new_content = content[0:prologue_end_index]
                    new_content += partial_injection_code
                    new_content += content[prologue_end_index:]
            else:
                tmp_index = direct_methods_start_index + len("# direct methods") + 1
                new_content = content[0:tmp_index]
                new_content += full_injection_code
                new_content += content[tmp_index:]

        # The newContent is ready to be saved

        with open(self.entrypoint_smali_path, "w", encoding="ascii") as smali_file:
            smali_file.write(new_content)

        self.logger.info("Frida loader was injected in the entrypoint smali file!")

        return True

    def create_lib_arch_folders(self, arch):
        """
        make lib folder in the apk to put native lib
        """
        # noinspection PyUnusedLocal
        sub_dir = None
        sub_dir_2 = None

        libs_path = self.final_dir / "lib"

        if not libs_path.is_dir():
            self.logger.info('There is no "lib" folder. Creating...')
            libs_path.mkdir(parents=True, exist_ok=True)

        if arch == self.ARCH_ARM:
            sub_dir = libs_path / "armeabi"
            sub_dir_2 = libs_path / "armeabi-v7a"

        elif arch == self.ARCH_ARM64:
            sub_dir = libs_path / "arm64-v8a"

        elif arch == self.ARCH_X86:
            sub_dir = libs_path / "x86"

        elif arch == self.ARCH_X64:
            sub_dir = libs_path / "x86_64"

        else:
            self.logger.error("Couldn't create the appropriate folder with the given arch.")
            return []

        if not sub_dir.is_dir():
            self.logger.info("Creating folder %s", sub_dir)
            sub_dir.mkdir(parents=True, exist_ok=True)

        if arch == self.ARCH_ARM:
            if not sub_dir_2.is_dir():
                self.logger.info("Creating folder %s", sub_dir_2)
                sub_dir_2.mkdir(parents=True, exist_ok=True)

        if arch == self.ARCH_ARM:
            return [sub_dir, sub_dir_2]
        return [sub_dir]

    def check_libextract(self) -> bool:
        """check if extractNativeLibs is enable and active it

        Returns:
            bool: return False if we didn't find manifest
        """
        self.logger.info("check if lib is extractable")

        manifest_path = self.final_dir / "AndroidManifest.xml"

        if not manifest_path.is_file():
            self.logger.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            return False

        with open(manifest_path, "rb") as fp:
            axml, _ = pyaxml.AXML.from_axml(fp.read())
            etree_xml = axml.to_xml()
            extract_native = etree_xml.findall(
                "./application/[@{http://schemas.android.com/apk/res/android}extractNativeLibs='false']"
            )
            if len(extract_native) > 0:
                extract_native[0].attrib[
                    "{http://schemas.android.com/apk/res/android}extractNativeLibs"
                ] = "true"

        with open(manifest_path, "wb") as fp:
            res_aml = pyaxml.axml.AXML()
            res_aml.from_xml(etree_xml)
            fp.write(res_aml.pack())
        return True

    def insert_frida_lib(
        self,
        gadget_path: str,
        arch: str,
        config_file_path=None,
        auto_load_script_path=None,
    ):
        """
        Insert native lib inside the apk

        Parameters:
                    - gadget_path (str): the path of the gadget to insert
        """
        arch_folders = self.create_lib_arch_folders(arch)

        if not arch_folders:
            self.logger.error("Some error occurred while creating the libs folders")
            return False

        for folder in arch_folders:
            if config_file_path and auto_load_script_path:
                self.delete_existing_gadget(
                    folder, delete_custom_files=self.CONFIG_BIT | self.AUTOLOAD_BIT
                )

            elif config_file_path and not auto_load_script_path:
                self.delete_existing_gadget(folder, delete_custom_files=self.CONFIG_BIT)

            elif auto_load_script_path and not config_file_path:
                self.delete_existing_gadget(folder, delete_custom_files=self.AUTOLOAD_BIT)

            else:
                self.delete_existing_gadget(folder, delete_custom_files=0)

            target_gadget_path = folder / self.DEFAULT_GADGET_NAME

            self.logger.info("Copying gadget to %s", target_gadget_path)

            shutil.copyfile(gadget_path, target_gadget_path)

            if config_file_path:
                target_config_path = target_gadget_path.replace(".so", ".config.so")

                self.logger.info("Copying config file to {target_config_path}")
                shutil.copyfile(config_file_path, target_config_path)

            if auto_load_script_path:
                target_autoload_path = target_gadget_path.replace(
                    self.DEFAULT_GADGET_NAME, self.DEFAULT_HOOKFILE_NAME
                )

                self.logger.info("Copying auto load script file to {target_autoload_path}")
                shutil.copyfile(auto_load_script_path, target_autoload_path)

        return True

    def delete_existing_gadget(self, arch_folder: Path, delete_custom_files: int = 0):
        """
        delete existing gadget inside the apk
        """
        gadget_path = arch_folder / self.DEFAULT_GADGET_NAME

        if gadget_path.is_file():
            gadget_path.unlink()

        if delete_custom_files & self.CONFIG_BIT:
            config_file_path: Path = arch_folder / self.DEFAULT_CONFIG_NAME

            if config_file_path.is_file():
                config_file_path.unlink()

        if delete_custom_files & self.AUTOLOAD_BIT:
            hookfile_path: Path = arch_folder / self.DEFAULT_HOOKFILE_NAME

            if hookfile_path.is_file():
                hookfile_path.unlink()

    ################################################################################
    #                                                                              #
    #                PATCHING                                                      #
    #                                                                              #
    ################################################################################

    def set_arch(self, arch: str):
        """set architecture of target phone where apk would be installed

        Args:
            arch (str): architecture
        """
        self.arch = arch

    def patching(
        self,
        gadget_to_use: str | None = None,
        output_file: Path | None = None,
        user_certificate: bool = False,
        splits_apk: list[Path] | None = None,
        entrypoint=None,
    ):
        """
        patch the apk with gadget 'gadget_to_use'
        """
        if splits_apk is None:
            splits_apk = []
        if len(self.network_certificates) > 0:
            user_certificate = True
        if not self.apk.is_file():
            self.logger.error("The file %s couldn't be found!", self.apk)
            sys.exit(1)

        # Create tempory file
        with tempfile.TemporaryDirectory() as tmp_dir:
            apk_name = Path(self.apk).stem
            self.final_dir = Path(f"{tmp_dir}/{apk_name}")

            # extract the apk on temporary folder
            self.extract_apk()

            # add Internet permission
            has_internet_permission = self.has_permission(self.INTERNET_PERMISSION)
            if not has_internet_permission:
                if not self.inject_permission_manifest(self.INTERNET_PERMISSION):
                    sys.exit(1)

            # add users certificate
            if user_certificate:
                with open(self.final_dir / "resources.arsc", "r+b") as fp:
                    rsc, _ = pyaxml.ARSC.from_axml(fp.read())
                    self.enable_user_certificates(rsc)
                    rsc.compute()
                    fp.seek(0)
                    fp.write(rsc.pack())

            # inject frida library
            if entrypoint is None:
                self.entrypoint_class = self.get_entrypoint_class_name()
                if self.entrypoint_class is None:
                    return
            else:
                self.entrypoint_class = entrypoint
            if not self.entrypoint_class:
                return
            self.entrypoint_smali_path = self.get_entrypoint_smali_path()
            if gadget_to_use:
                self.insert_frida_loader()
            if not self.check_libextract():
                return

            if gadget_to_use:
                if not self.arch:
                    archs = [
                        (plba(gadget_to_use, self.ARCH_ARM), self.ARCH_ARM),
                        (plba(gadget_to_use, self.ARCH_ARM64), self.ARCH_ARM64),
                        (plba(gadget_to_use, self.ARCH_X86), self.ARCH_X86),
                        (plba(gadget_to_use, self.ARCH_X86_64), self.ARCH_X64),
                    ]
                else:
                    archs = [(gadget_to_use, self.arch)]
                for gadget, arch in archs:
                    self.insert_frida_lib(gadget, arch)

            # repackage the apk and sign + align it
            if output_file:
                output_file_path = self.repackage_apk(target_file=output_file)

            else:
                output_file_path = self.repackage_apk()

            self.sign_and_zipalign(output_file_path, splits_apk)

    @staticmethod
    def get_default_config_file() -> Path:
        """
        get a default config to frida to auto start frida at launch
        """

        config: str = f"""
{
    "interaction": {
        "type": "script",
        "address": "127.0.0.1",
        "port": 27042,
        "path": "./libhook.js.so"
    }
}
        """

        path = Path.cwd() / "generatedConfigFile.config"
        with open(path, "w", encoding="ascii") as f:
            f.write(config)

        return path
