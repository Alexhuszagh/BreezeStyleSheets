from pathlib import Path

import pytest


@pytest.fixture
def test_dir() -> Path:
    return Path(__file__).parent


@pytest.fixture
def data_dir(test_dir: Path) -> Path:
    return test_dir / 'data'


@pytest.fixture
def project_dir(test_dir: Path) -> Path:
    return test_dir.parent
