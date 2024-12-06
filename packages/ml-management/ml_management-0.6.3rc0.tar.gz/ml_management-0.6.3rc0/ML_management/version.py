from importlib.metadata import version

try:
    __version__ = version("ml-management")
except Exception:
    __version__ = "unknown"
