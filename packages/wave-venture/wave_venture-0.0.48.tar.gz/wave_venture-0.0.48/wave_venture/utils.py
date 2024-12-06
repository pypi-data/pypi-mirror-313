import os
import sys
import pytz
import json
import asyncio
import datetime
import functools


ALL_METATYPES = {
    "body",
}


def is_document(obj):
    return isinstance(obj, dict) and obj.get("_type") == "doc"


def assert_call_signature(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if len(args) == 0:
            raise ValueError(
                "insert must be called with a metatype name 'doc', 'body', etc as it's first positional argument."
            )

        _metatype = args[0]

        if _metatype == "doc" and len(args) == 1:
            return f(*args, **kwargs)
        elif _metatype in ALL_METATYPES and len(args) == 2 and is_document(args[1]):
            return f(*args, **kwargs)
        elif _metatype == "doc" and len(args) > 1:
            raise ValueError(
                'when inserting a doc, all arguments following "doc" must be keyword arguments. e.g. di.insert("doc", name="my_new_doc")'
            )
        elif _metatype not in ALL_METATYPES:
            raise ValueError(f"unknown prototype '{_metatype}'")
        elif len(args) > 2:
            raise ValueError(
                'when inserting a prototype, all arguments following the prototype name and the document must be keyword arguments. e.g. di.insert("body", doc, name="my_new_doc")'
            )
        else:
            raise ValueError("incorrect call")

    return wrapper


WIN_GUI_LOCAL_PATHS = (
    r"~\AppData\Local\Wave Venture\Wave Venture TE\offline\local.json",
)
MAC_GUI_LOCAL_PATHS = (
    r"~/Library/Preferences/Wave Venture/Wave Venture TE/offline/local.json",
)
LINUX_GUI_LOCAL_PATHS = (
    r"/etc/xdg/Wave Venture/Wave Venture TE/offline/local.json",
    r"~/.config/Wave Venture/Wave Venture TE/offline/local.json",
)


def find_auth_token():
    path_candidates = []
    if sys.platform.startswith("win"):
        path_candidates = WIN_GUI_LOCAL_PATHS
    elif sys.platform == "darwin":
        path_candidates = MAC_GUI_LOCAL_PATHS
    else:
        path_candidates = LINUX_GUI_LOCAL_PATHS

    for path in path_candidates:
        path = os.path.expanduser(path)
        try:
            with open(path, "r") as fp:
                local = json.load(fp)

            return local["server"]["token"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass


WIN_GUI_REGISTRY_PATH = (
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\wv_gui_is1"
)
MAC_GUI_PLOTTER_PATH = "/Applications/Wave Venture TE.app/Contents/MacOS/wv_plotter"
LINUX_GUI_PLOTTER_PATH = "/usr/bin/wv_plotter"


def find_gui_plotter():
    if sys.platform.startswith("win"):
        import winreg

        possible_keys = [
            # HKEY_CURRENT_USER for non admin install
            # (like corporate computer without admin right)
            winreg.HKEY_CURRENT_USER,
            # - HKEY_LOCAL_MACHINE for admin installation
            # (most of home computer where the user is the admin)
            winreg.HKEY_LOCAL_MACHINE,
        ]

        for key in possible_keys:
            try:
                with winreg.OpenKey(key, WIN_GUI_REGISTRY_PATH) as key:
                    path, _ = winreg.QueryValueEx(key, "InstallLocation")
            except FileNotFoundError:
                continue

            path = os.path.join(path, "wv_plotter.exe")
            if os.path.exists(path):
                return path
    elif sys.platform == "darwin" and os.path.exists(MAC_GUI_PLOTTER_PATH):
        return MAC_GUI_PLOTTER_PATH
    elif os.path.exists(LINUX_GUI_PLOTTER_PATH):
        return LINUX_GUI_PLOTTER_PATH


def serial(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper


EPOCH = datetime.datetime(1970, 1, 1)
UTC_EPOCH = EPOCH.replace(tzinfo=datetime.timezone.utc)


def to_epoch(dt):
    return (dt - EPOCH).total_seconds()


def from_epoch(seconds):
    return datetime.datetime.utcfromtimestamp(0) + datetime.timedelta(seconds=seconds)


def hours_between(d1, d2):
    return (d2 - d1).total_seconds() / 60 / 60


def is_date(d):
    if isinstance(d, datetime.date):
        return True
    elif isinstance(d, datetime.datetime):
        date_resolution = datetime.datetime(year=d.year, month=d.month, day=d.day)
        return d == date_resolution
    else:
        raise ValueError(f"Expecting datetime.datetime or datetime.date, got {type(d)}")


def is_naive(d):
    return not (d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None)


def is_utc(d):
    return d.tzinfo == datetime.timezone.utc or d.tzinfo == pytz.utc
