def get_root_module_name(symbol_path: str) -> str:
    """Return the name of the root module (without dots) where *symbol_path* is the ``__name__`` of one of its symbols (e.g. submodule, class, function, etc.)."""
    return symbol_path.split(".", maxsplit=1)[0]
