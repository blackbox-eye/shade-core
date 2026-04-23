import importlib


def test_import_smoke() -> None:
    module = importlib.import_module("shade_core")

    assert module.__version__ == "0.1.0"