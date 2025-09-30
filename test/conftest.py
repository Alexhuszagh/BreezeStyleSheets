from pathlib import Path

import pytest
from breezestylesheets import utils


@pytest.fixture
def project_dir() -> Path:
    return utils.project_dir()


@pytest.fixture
def test_dir(project_dir: Path) -> Path:
    return project_dir / 'test'


@pytest.fixture
def data_dir(test_dir: Path) -> Path:
    return test_dir / 'data'
