import tarfile

import requests
from loguru import logger

from .cache import get_deps_cache
from .shell import add_path_to_shell

VERIBLE_MAC_OS_LINK = "https://github.com/chipsalliance/verible/releases/download/v0.0-3752-g8b64887e/verible-v0.0-3752-g8b64887e-macOS.tar.gz"
VERIBLE_WINDOWS_64_OS_LINK = "https://github.com/chipsalliance/verible/releases/download/v0.0-3752-g8b64887e/verible-v0.0-3752-g8b64887e-win64.zip"
VERIBLE_LINUX_X86_64_OS_LINK = "https://github.com/chipsalliance/verible/releases/download/v0.0-3752-g8b64887e/verible-v0.0-3752-g8b64887e-linux-static-x86_64.tar.gz"
VERIBLE_LINUX_ARM64_LINK = "https://github.com/chipsalliance/verible/releases/download/v0.0-3752-g8b64887e/verible-v0.0-3752-g8b64887e-linux-static-arm64.tar.gz"


def install_verible(system_info: dict) -> str:
    url = None
    if system_info.get("os_family") == "Darwin":
        url = VERIBLE_MAC_OS_LINK
    elif system_info.get("os_family") == "Windows":
        url = VERIBLE_WINDOWS_64_OS_LINK
    elif system_info.get("processor") == "x86_64":
        url = VERIBLE_LINUX_X86_64_OS_LINK
    elif system_info.get("processor") == "arm":
        url = VERIBLE_LINUX_X86_64_OS_LINK

    deps_cache = get_deps_cache()

    verible_dir_name = url.split("/")[-1].split(".tar.gz")[0]
    file_download_path = deps_cache / f"{verible_dir_name}.tar.gz"

    logger.debug("Downloading verible")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_download_path, "wb") as file:
            file.write(response.raw.read())
    else:
        raise Exception(
            f"Failed to download verible. {response.status_code}. {response.text}"
        )

    logger.debug("Untaring verible")
    with tarfile.open(file_download_path) as tar:
        tar.extractall(deps_cache)

    logger.debug("Deleting tar.gz artifact")
    file_download_path.unlink()

    unpacked_verible_dir_name = verible_dir_name
    if "linux" in unpacked_verible_dir_name:
        unpacked_verible_dir_name = unpacked_verible_dir_name.split("-linux")[0]

    verible_bin = deps_cache.joinpath(unpacked_verible_dir_name).joinpath("bin")

    logger.debug("Adding verible to PATH")
    add_path_to_shell(verible_bin)

    return verible_bin
