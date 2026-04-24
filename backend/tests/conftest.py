import sys
from pathlib import Path

import pytest

# Ensure `backend/` is on path when running tests from repo root
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


@pytest.fixture
def client(tmp_path):
    from app import create_app

    return create_app(patient_file=tmp_path / "patients.json").test_client()
