import os
import platform
import shutil
import subprocess
import tempfile
import zipfile
from io import BytesIO

import requests
from retry import retry

from t_vault.utils import exceptions
from t_vault.utils.logger import logger

PLATFORMS = {"linux": "linux", "darwin": "macos", "windows": "windows"}
OS_NAME = PLATFORMS.get(platform.system().lower())


@retry(exceptions=(exceptions.BitwardenDownloadError,), tries=3, delay=2, backoff=2)
def download_from_bw_site() -> requests.Response:
    """Downloads the Bitwarden CLI app for the specified operating system.

    Returns:
        requests.Response: The response object from the download request.
    """
    url = f"https://vault.bitwarden.com/download/?app=cli&platform={OS_NAME}"
    try:
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
    except requests.RequestException as e:
        raise exceptions.BitwardenDownloadError(f"Failed to download Bitwarden: {r.status_code}") from e
    return r


@retry(exceptions=(exceptions.BitwardenDownloadError,), tries=3, delay=2, backoff=2)
def download_from_aws(force_latest=False) -> requests.Response:
    """Downloads the Bitwarden CLI app for the specified operating system from AWS.

    Args:
        force_latest (bool, optional): If True, download the latest version of the Bitwarden CLI. Defaults to False.

    Returns:
        requests.Response: The response object from the download request.
    """
    if force_latest:
        url = f"https://bitwarden-cli.s3.amazonaws.com/bw-{OS_NAME}.zip"
    else:
        url = f"https://bitwarden-cli.s3.amazonaws.com/bw-{OS_NAME}-stable.zip"
    try:
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
    except requests.RequestException as e:
        raise exceptions.BitwardenDownloadError(f"Failed to download Bitwarden from AWS: {r.status_code}") from e
    return r


def get_scripts_path() -> str:
    """Returns the path to the virtual environment's bin directory.

    If not in a virtual environment, returns the current working directory.

    Returns:
        str: The path to the virtual environment's bin directory.
    """
    if not (venv_path := os.getenv("VIRTUAL_ENV") or os.getenv("CONDA_PREFIX")):
        return os.getcwd()

    scripts_dir = "Scripts" if OS_NAME == "windows" else "bin"
    return os.path.join(
        venv_path,
        scripts_dir,
    )


def is_bitwarden_installed() -> bool:
    """Checks if the Bitwarden CLI is installed.

    Returns:
        bool: True if the Bitwarden CLI is installed, False otherwise.
    """
    exe_file = "bw" if OS_NAME != "windows" else "bw.exe"
    exe_path = os.path.join(get_scripts_path(), exe_file)

    return os.path.exists(exe_path)


def install_bitwarden(force_latest=False) -> str:
    """Downloads the Bitwarden CLI if not already installed and returns the path to the executable.

    Args:
        force_latest (bool, optional): If True, download the latest version of the Bitwarden CLI. Defaults to False.

    Returns:
        str: The path to the Bitwarden CLI executable.

    Raises:
        exceptions.UnsupportedPlatformException: If the OS is not supported.
        exceptions.BitwardenDownloadError: If an error occurs during the download.
    """
    logger.info("Downloading Bitwarden CLI.")
    exe_file = "bw" if OS_NAME != "windows" else "bw.exe"

    scripts_path = get_scripts_path()

    if is_bitwarden_installed():
        os.remove(os.path.join(scripts_path, exe_file))

    if OS_NAME is None:
        raise exceptions.UnsupportedPlatformException(f"Unsupported OS: {platform.system()}")
    try:
        if OS_NAME == "macos":
            response = download_from_bw_site()
        else:
            response = download_from_aws(force_latest)
    except exceptions.BitwardenDownloadError:
        if OS_NAME == "macos":
            response = download_from_aws(force_latest)
        else:
            response = download_from_bw_site()

    # Extract the downloaded zip file
    with tempfile.TemporaryDirectory() as temp_path:
        zipfile.ZipFile(BytesIO(response.content)).extractall(temp_path)

        path_to_exe = os.path.join(temp_path, exe_file)

        if OS_NAME != "windows":
            subprocess.run(["chmod", "+x", path_to_exe], capture_output=True, text=True)
        if OS_NAME == "macos":
            subprocess.run(["xattr", "-d", "com.apple.quarantine", path_to_exe], capture_output=True, text=True)

        shutil.move(path_to_exe, scripts_path)

    return os.path.join(scripts_path, exe_file)


def get_bw_path() -> str:
    """Returns the path to the Bitwarden CLI executable.

    Returns:
        str: The path to the Bitwarden CLI executable.

    Raises:
        exceptions.BitwardenNotInstalledError: If the Bitwarden CLI is not installed.
    """
    exe_file = "bw" if OS_NAME != "windows" else "bw.exe"
    exe_path = os.path.join(get_scripts_path(), exe_file)

    if not is_bitwarden_installed():
        raise exceptions.BitwardenNotInstalledError("Bitwarden CLI is not installed.")

    return exe_path
