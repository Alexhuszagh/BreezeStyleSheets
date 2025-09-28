from pathlib import Path

import pytest
from breezestylesheets import config


@pytest.mark.parametrize(
    'filename',
    ['default.json'],
)
def test_load(data_dir: Path, filename: str) -> None:
    loaded = config.load(data_dir / filename)
    _ = loaded.model_dump()
    _ = loaded.model_dump_json()
