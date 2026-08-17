from dataclasses import asdict
from pathlib import Path

import pytest

from breezestylesheets.model import loads_json
from breezestylesheets.theme import Theme


@pytest.mark.parametrize(
    "filename",
    ["default.json"],
)
def test_load_theme(data_dir: "Path", filename: "str") -> "None":
    file = data_dir / filename
    data = loads_json(file.read_text())
    loaded = Theme.load(file)
    assert loaded == Theme.validate(data)


def test_load_theme_all(project_dir: "Path") -> "None":
    for file in (project_dir / "theme").glob("*.json"):
        data = loads_json(file.read_text())
        loaded = Theme.load(file)
        assert loaded == Theme.validate(data)
        _ = asdict(loaded)
