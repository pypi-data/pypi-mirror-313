import platform
import sys
import re
import subprocess
import os
import zipfile
import tarfile
from lazysdk import lazyfile

# from webdriver_manager.core.utils import linux_browser_apps_to_cmd, windows_browser_apps_to_cmd, \
#     read_version_from_cmd

"""
借鉴webdriver_manager==4.0.1代码，但是原模块不好用，所以这里精简了
"""
ROOT_FOLDER_NAME = ".lazy_chromedriver"
DEFAULT_PROJECT_ROOT_CACHE_PATH = os.path.join(sys.path[0], ROOT_FOLDER_NAME)
DEFAULT_USER_HOME_CACHE_PATH = os.path.join(os.path.expanduser("~"), ROOT_FOLDER_NAME)
drivers_root = "drivers"
drivers_directory = os.path.join(DEFAULT_USER_HOME_CACHE_PATH, drivers_root)


def determine_powershell():
    """Returns "True" if runs in Powershell and "False" if another console."""
    cmd = "(dir 2>&1 *`|echo CMD);&<# rem #>echo powershell"
    with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            shell=True,
    ) as stream:
        stdout = stream.communicate()[0].decode()
    return "" if stdout == "powershell" else "powershell"


def linux_browser_apps_to_cmd(*apps: str) -> str:
    """Create 'browser --version' command from browser app names.

    Result command example:
        chromium --version || chromium-browser --version
    """
    ignore_errors_cmd_part = " 2>/dev/null" if os.getenv(
        "WDM_LOG_LEVEL") == "0" else ""
    return " || ".join(f"{i} --version{ignore_errors_cmd_part}" for i in apps)


def windows_browser_apps_to_cmd(*apps: str) -> str:
    """Create analogue of browser --version command for windows."""
    powershell = determine_powershell()

    first_hit_template = """$tmp = {expression}; if ($tmp) {{echo $tmp; Exit;}};"""
    script = "$ErrorActionPreference='silentlycontinue'; " + " ".join(
        first_hit_template.format(expression=e) for e in apps
    )

    return f'{powershell} -NoProfile "{script}"'


def read_version_from_cmd(cmd, pattern):
    with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            shell=True,
    ) as stream:
        stdout = stream.communicate()[0].decode()
        version = re.search(pattern, stdout)
        version = version.group(0) if version else None
    return version


class ChromeType(object):
    GOOGLE = "google-chrome"
    CHROMIUM = "chromium"
    BRAVE = "brave-browser"
    MSEDGE = "edge"


class OSType(object):
    LINUX = "linux"
    MAC = "mac"
    WIN = "win"


PATTERN = {
    ChromeType.CHROMIUM: r"\d+\.\d+\.\d+",
    ChromeType.GOOGLE: r"\d+\.\d+\.\d+.\d+",  # 增加了最小版本
    ChromeType.MSEDGE: r"\d+\.\d+\.\d+",
    "brave-browser": r"\d+\.\d+\.\d+(\.\d+)?",
    "firefox": r"(\d+.\d+)",
}


def get_os_name():
    pl = sys.platform
    if pl == "linux" or pl == "linux2":
        return OSType.LINUX
    elif pl == "darwin":
        return OSType.MAC
    elif pl == "win32" or pl == "cygwin":
        return OSType.WIN


def get_os_type():
    pl = sys.platform
    if pl == "darwin":
        return f'mac-{platform.machine()}'
    elif pl == "win32" or pl == "cygwin":
        if platform.machine().endswith("64"):
            return 'win64'
        else:
            return 'win32'


class OperationSystemManager(object):

    def __init__(self, os_type=None):
        self._os_type = os_type

    @staticmethod
    def get_os_name():
        pl = sys.platform
        if pl == "linux" or pl == "linux2":
            return OSType.LINUX
        elif pl == "darwin":
            return OSType.MAC
        elif pl == "win32" or pl == "cygwin":
            return OSType.WIN

    @staticmethod
    def get_os_architecture():
        if platform.machine().endswith("64"):
            return 64
        else:
            return 32

    def get_os_type(self):
        if self._os_type:
            return self._os_type
        return f"{self.get_os_name()}{self.get_os_architecture()}"

    @staticmethod
    def is_arch(os_sys_type):
        if '_m1' in os_sys_type:
            return True
        return platform.processor() != 'i386'

    @staticmethod
    def is_mac_os(os_sys_type):
        return OSType.MAC in os_sys_type

    def get_browser_version_from_os(self, browser_type=None):
        """Return installed browser version."""
        cmd_mapping = {
            ChromeType.GOOGLE: {
                OSType.LINUX: linux_browser_apps_to_cmd(
                    "google-chrome",
                    "google-chrome-stable",
                    "google-chrome-beta",
                    "google-chrome-dev",
                ),
                OSType.MAC: r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",
                OSType.WIN: windows_browser_apps_to_cmd(
                    r'(Get-Item -Path "$env:PROGRAMFILES\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion',
                    r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion',
                    r'(Get-Item -Path "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion',
                    r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Google\Chrome\BLBeacon").version',
                    r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome").version',
                ),
            },
            ChromeType.CHROMIUM: {
                OSType.LINUX: linux_browser_apps_to_cmd("chromium", "chromium-browser"),
                OSType.MAC: r"/Applications/Chromium.app/Contents/MacOS/Chromium --version",
                OSType.WIN: windows_browser_apps_to_cmd(
                    r'(Get-Item -Path "$env:PROGRAMFILES\Chromium\Application\chrome.exe").VersionInfo.FileVersion',
                    r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Chromium\Application\chrome.exe").VersionInfo.FileVersion',
                    r'(Get-Item -Path "$env:LOCALAPPDATA\Chromium\Application\chrome.exe").VersionInfo.FileVersion',
                    r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Chromium\BLBeacon").version',
                    r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Chromium").version',
                ),
            },
            ChromeType.BRAVE: {
                OSType.LINUX: linux_browser_apps_to_cmd(
                    "brave-browser", "brave-browser-beta", "brave-browser-nightly"
                ),
                OSType.MAC: r"/Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --version",
                OSType.WIN: windows_browser_apps_to_cmd(
                    r'(Get-Item -Path "$env:PROGRAMFILES\BraveSoftware\Brave-Browser\Application\brave.exe").VersionInfo.FileVersion',
                    r'(Get-Item -Path "$env:PROGRAMFILES (x86)\BraveSoftware\Brave-Browser\Application\brave.exe").VersionInfo.FileVersion',
                    r'(Get-Item -Path "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\Application\brave.exe").VersionInfo.FileVersion',
                    r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\BraveSoftware\Brave-Browser\BLBeacon").version',
                    r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\BraveSoftware Brave-Browser").version',
                ),
            },
            ChromeType.MSEDGE: {
                OSType.LINUX: linux_browser_apps_to_cmd(
                    "microsoft-edge",
                    "microsoft-edge-stable",
                    "microsoft-edge-beta",
                    "microsoft-edge-dev",
                ),
                OSType.MAC: r"/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version",
                OSType.WIN: windows_browser_apps_to_cmd(
                    # stable edge
                    r'(Get-Item -Path "$env:PROGRAMFILES\Microsoft\Edge\Application\msedge.exe").VersionInfo.FileVersion',
                    r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Microsoft\Edge\Application\msedge.exe").VersionInfo.FileVersion',
                    r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Microsoft\Edge\BLBeacon").version',
                    r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Microsoft\EdgeUpdate\Clients\{56EB18F8-8008-4CBD-B6D2-8C97FE7E9062}").pv',
                    # beta edge
                    r'(Get-Item -Path "$env:LOCALAPPDATA\Microsoft\Edge Beta\Application\msedge.exe").VersionInfo.FileVersion',
                    r'(Get-Item -Path "$env:PROGRAMFILES\Microsoft\Edge Beta\Application\msedge.exe").VersionInfo.FileVersion',
                    r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Microsoft\Edge Beta\Application\msedge.exe").VersionInfo.FileVersion',
                    r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Microsoft\Edge Beta\BLBeacon").version',
                    # dev edge
                    r'(Get-Item -Path "$env:LOCALAPPDATA\Microsoft\Edge Dev\Application\msedge.exe").VersionInfo.FileVersion',
                    r'(Get-Item -Path "$env:PROGRAMFILES\Microsoft\Edge Dev\Application\msedge.exe").VersionInfo.FileVersion',
                    r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Microsoft\Edge Dev\Application\msedge.exe").VersionInfo.FileVersion',
                    r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Microsoft\Edge Dev\BLBeacon").version',
                    # canary edge
                    r'(Get-Item -Path "$env:LOCALAPPDATA\Microsoft\Edge SxS\Application\msedge.exe").VersionInfo.FileVersion',
                    r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Microsoft\Edge SxS\BLBeacon").version',
                    # highest edge
                    r"(Get-Item (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe').'(Default)').VersionInfo.ProductVersion",
                    r"[System.Diagnostics.FileVersionInfo]::GetVersionInfo((Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe').'(Default)').ProductVersion",
                    r"Get-AppxPackage -Name *MicrosoftEdge.* | Foreach Version",
                    r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge").version',
                ),
            },
            "firefox": {
                OSType.LINUX: linux_browser_apps_to_cmd("firefox"),
                OSType.MAC: r"/Applications/Firefox.app/Contents/MacOS/firefox --version",
                OSType.WIN: windows_browser_apps_to_cmd(
                    r'(Get-Item -Path "$env:PROGRAMFILES\Mozilla Firefox\firefox.exe").VersionInfo.FileVersion',
                    r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Mozilla Firefox\firefox.exe").VersionInfo.FileVersion',
                    r"(Get-Item (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe').'(Default)').VersionInfo.ProductVersion",
                    r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Mozilla\Mozilla Firefox").CurrentVersion',
                ),
            },
        }

        try:
            cmd_mapping = cmd_mapping[browser_type][OperationSystemManager.get_os_name()]
            pattern = PATTERN[browser_type]
            version = read_version_from_cmd(cmd_mapping, pattern)
            return version
        except Exception:
            return None
            # raise Exception("Can not get browser version from OS")


def get_driver_download_url(
        driver_url='https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing',
):
    os_type = get_os_type()
    driver_version = OperationSystemManager().get_browser_version_from_os(browser_type='google-chrome')
    return f"{driver_url}/{driver_version}/{os_type}/chromedriver-{os_type}.zip"


# def save_archive_file(file: File, directory: str):
#     os.makedirs(directory, exist_ok=True)
#
#     archive_path = f"{directory}{os.sep}{file.filename}"
#     with open(archive_path, "wb") as code:
#         code.write(file.content)
#     if not os.path.exists(archive_path):
#         raise FileExistsError(f"No file has been saved on such path {archive_path}")
#     return Archive(archive_path)
#
#
def download_driver():
    """
    根据当前系统的chrome版本下载对应版本的driver
    """
    from lazysdk import lazyfile
    driver_download_url = get_driver_download_url()
    os.makedirs(drivers_directory, exist_ok=True)  # 创建driver下载目录
    filename = extract_filename_from_url(driver_download_url)
    print('filename:', filename)
    archive_path = os.path.join(drivers_directory, filename)
    # archive_path = f"{directory}{os.sep}{file.filename}"
    print(driver_download_url)
    file = lazyfile.download(
        url=driver_download_url,
        filename=filename,
        path=drivers_directory
    )['file_dir']
    return unpack_archive(archive_file=file, target_dir=drivers_directory)


class LinuxZipFileWithPermissions(zipfile.ZipFile):
    """Class for extract files in linux with right permissions"""

    def extract(self, member, path=None, pwd=None):
        if not isinstance(member, zipfile.ZipInfo):
            member = self.getinfo(member)

        if path is None:
            path = os.getcwd()

        ret_val = self._extract_member(member, path, pwd)  # noqa
        attr = member.external_attr >> 16
        os.chmod(ret_val, attr)
        return ret_val


def unpack_archive(archive_file, target_dir):
    if archive_file.endswith(".zip"):
        return lazyfile.unzip(file=archive_file)
    elif archive_file.endswith(".tar.gz"):
        return __extract_tar_file(archive_file, target_dir)


def __extract_zip(archive_file, to_directory):
    zip_class = zipfile.ZipFile
    archive = zip_class(archive_file)
    try:
        archive.extractall(to_directory)
    except Exception as e:
        if e.args[0] not in [26, 13] and e.args[1] not in [
            "Text file busy",
            "Permission denied",
        ]:
            raise e
        file_names = []
        for n in archive.namelist():
            if "/" not in n:
                file_names.append(n)
            else:
                file_path, file_name = n.split("/")
                full_file_path = os.path.join(to_directory, file_path)
                source = os.path.join(full_file_path, file_name)
                destination = os.path.join(to_directory, file_name)
                os.replace(source, destination)
                file_names.append(file_name)
        return sorted(file_names, key=lambda x: x.lower())
    return archive.namelist()


def __extract_tar_file(archive_file, to_directory):
    try:
        tar = tarfile.open(archive_file.file_path, mode="r:gz")
    except tarfile.ReadError:
        tar = tarfile.open(archive_file.file_path, mode="r:bz2")
    members = tar.getmembers()
    tar.extractall(to_directory)
    tar.close()
    return [x.name for x in members]


def extract_filename_from_url(url):
    """
    从url中获取文件名
    """
    # Split the URL by '/'
    url_parts = url.split('/')
    # Get the last part of the URL, which should be the filename
    filename = url_parts[-1]
    # Decode the URL-encoded filename
    filename = os.path.basename(filename)
    return filename
