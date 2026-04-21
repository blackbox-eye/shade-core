from pathlib import Path
import importlib
import sys


def test_import_smoke() -> None:
    src_path = Path(__file__).resolve().parents[1] / "src"
    sys.path.insert(0, str(src_path))

    module = importlib.import_module("shade_core")

    assert module.__version__ == "0.1.0"