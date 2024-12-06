try:
    import importlib.metadata

    __version__ = importlib.metadata.version("truefoundry")
except Exception:
    __version__ = "NA"
