import getpass
import os
import pathlib
import platform
import time
from configparser import RawConfigParser


class GetCfg:
    """Gets the value in the configuration file"""

    def __init__(self, config_file: str, option: [str, None] = None):
        self.config_file = config_file
        self.option = option
        self.conf = RawConfigParser()
        self.conf.read(self.config_file, encoding="utf-8")

    def get(self, key: str, op: [str, None] = None, default=None) -> str:
        if op is None and self.option is not None:
            op = self.option
        if op is None and self.option is None:
            raise ValueError("option is None")
        return self.conf.get(op, key, fallback=default)

    def get_bool(self, key: str, op: [str, None] = None, default=False) -> bool:
        if op is None and self.option is not None:
            op = self.option
        if op is None and self.option is None:
            raise ValueError("option is None")
        return self.conf.getboolean(op, key, fallback=default)


class ArchName:
    x86 = "x86_64"
    aarch64 = "aarch64"
    loongarch64 = "loongarch64"
    mips64 = "mips64"
    sw64 = "sw64"


class DisplayServer:
    wayland = "wayland"
    x11 = "x11"


class _DynamicSetting:
    SYS_ARCH = platform.machine().lower()
    HOME = str(pathlib.Path.home())
    USERNAME = getpass.getuser()

    YOUQU_HOME = pathlib.Path(__file__).parent.parent
    TPL_PATH = YOUQU_HOME / "tpl"

    if os.path.exists(os.path.expanduser("~/.xsession-errors")):
        DISPLAY_SERVER = (
            os.popen("cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1")
            .read()
            .split("=")[-1]
            .strip("\n")
        )
    else:
        DISPLAY_SERVER = "x11" if os.popen("ps -ef | grep -v grep | grep kwin_x11").read() else "wayland"

    IS_X11: bool = DISPLAY_SERVER == DisplayServer.x11
    IS_WAYLAND: bool = DISPLAY_SERVER == DisplayServer.wayland

    TIME_STRING = time.strftime("%Y%m%d%H%M%S")
    HOST_IP = str(os.popen("hostname -I |awk '{print $1}'").read()).strip("\n").strip()

    VERSION = ""
    if os.path.exists("/etc/os-version"):
        version_cfg = GetCfg("/etc/os-version", "Version")
        VERSION = (version_cfg.get("EditionName[zh_CN]") or "") + (
                version_cfg.get("MinorVersion") or ""
        )
