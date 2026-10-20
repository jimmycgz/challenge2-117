try:
    from . import agent  # noqa: F401  (ADK discovers `root_agent` through this)
except ModuleNotFoundError as _exc:
    if not (_exc.name or "").startswith("google"):
        raise

