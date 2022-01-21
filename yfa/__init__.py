try:
    VERSION = __import__("pkg_resources").get_distribution("dispatch").version
except Exception:
    VERSION = "unknown"

__version__ = VERSION
