import argparse
import logging
import sys
from pathlib import Path
from apkpatcher import Patcher, conf, new_logger


def main() -> int:
    """cli function"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--apk", help="Specify the apk you want to patch")
    parser.add_argument("-m", "--multiple_split", nargs="*", help="provided multiple split apks")
    parser.add_argument(
        "-g",
        "--gadget",
        help="Specify the frida-gadget file \
                        file.so or file with no architecture specified will be \
                        autocomplete with file_<arch>.so",
    )
    parser.add_argument("-s", "--sdktools", help="Path of the sdktools")
    parser.add_argument("-b", "--version_buildtools", help="version for buildtools")
    parser.add_argument(
        "-r",
        "--arch",
        choices=[
            Patcher.ARCH_ARM,
            Patcher.ARCH_ARM64,
            Patcher.ARCH_X86,
            Patcher.ARCH_X64,
        ],
        help="architecture targeted",
    )
    parser.add_argument(
        "-v", "--verbosity", help="Verbosity level (0 to 3). Default is 3", type=int
    )

    parser.add_argument(
        "-e",
        "--enable-user-certificates",
        help="Add some configs in apk to accept user certificates",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--custom-certificate",
        help="Install a custom network certificate inside the apk",
    )

    parser.add_argument("-o", "--output-file", help="Specify the output file (patched)")

    parser.add_argument("-p", "--pause", help="pause before repackage the apk", action="store_true")
    parser.add_argument(
        "--plugin",
        help="execute load plugin (a python file with as argument the folder before the packaging)",
    )
    parser.add_argument("-V", "--version", help="version of apkpatcher", action="store_true")
    parser.add_argument(
        "--entrypoint",
        help="specify the class name where you want to inject your library",
    )

    args = parser.parse_args()

    if args.version:
        print(f"version {conf.VERSION}")
        return 0

    if len(sys.argv) == 1 or not (args.apk and args.sdktools and args.version_buildtools):
        print("apkpatcher -a <apk> -s <sdktools> -b <version> [options]")
        if not args.apk:
            print("\nArgument apk is missing, you should add '-a myapk.apk'")
        if not args.sdktools:
            print("\nArgument sdktools is missing, you should add '-s /usr/lib/android-sdk'")
            print(
                "If you didn't have installed sdktools follow this tutorial: https://madsquirrels.gitlab.io/mobile/asthook/how.install.html#setup-sdktools"
            )
        if not args.version_buildtools:
            print("\nArgument version_buildtools is missing, you should add '-b 30.0.2'")
            print("To know buildtools installed you can use: sdkmanager --list")
        parser.print_help()
        return 1

    logger = None
    if args.verbosity:
        if args.verbosity == 3:
            logger = new_logger(logging.DEBUG)
        elif args.verbosity == 2:
            logger = new_logger(logging.INFO)
        else:
            logger = new_logger(logging.ERROR)
    else:
        logger = new_logger(logging.INFO)
    patcher = Patcher(args.apk, args.sdktools, args.version_buildtools, logger)
    if patcher.check_binaries_tools_installed() == -1:
        logger.error("some binaries is missing")
        return 1
    if args.custom_certificate:
        patcher.add_network_certificate(Path(args.custom_certificate))
    if args.arch:
        patcher.set_arch(args.arch)
    patcher.pause(args.pause)
    if args.plugin:
        patcher.set_plugin(args.plugin)
    if args.multiple_split:
        splits_apk = args.multiple_split
    else:
        splits_apk = []
    if args.entrypoint:
        entrypoint = args.entrypoint
    else:
        entrypoint = None

    if args.output_file:
        patcher.patching(
            args.gadget,
            output_file=Path(args.output_file),
            user_certificate=args.enable_user_certificates,
            splits_apk=splits_apk,
            entrypoint=entrypoint,
        )
    else:
        patcher.patching(
            args.gadget,
            user_certificate=args.enable_user_certificates,
            splits_apk=splits_apk,
            entrypoint=entrypoint,
        )
    return 0
