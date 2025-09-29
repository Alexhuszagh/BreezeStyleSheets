from pathlib import Path

import pytest
from breezestylesheets import config


@pytest.mark.parametrize(
    'filename',
    ['default.json'],
)
def test_load_theme(data_dir: Path, filename: str) -> None:
    loaded = config.Theme.load(data_dir / filename)
    _ = loaded.model_dump()
    _ = loaded.model_dump_json()


def test_load_theme_all(project_dir: Path) -> None:
    for file in (project_dir / 'theme').glob('*.json'):
        loaded = config.Theme.load(file)
        _ = loaded.model_dump()
        _ = loaded.model_dump_json()
