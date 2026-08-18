from breezestylesheets.style import Style
from breezestylesheets.utils import template_dir, theme_dir


def test_find_styles() -> None:
    styles = Style.find_styles(theme_dir())
    assert len(styles) > 2
    assert theme_dir() / "dark-blue.json" in styles
    assert theme_dir() / "light-blue.json" in styles

    styles = Style.find_styles(theme_dir(), subset=set())
    assert not styles

    styles = Style.find_styles(theme_dir(), subset={"dark-blue"})
    assert len(styles) == 1
    assert theme_dir() / "dark-blue.json" in styles


def test_find_extensions() -> None:
    extensions = Style.find_extensions(template_dir())
    assert len(extensions) > 2
    assert template_dir() / "advanced-docking-system" in extensions
    assert template_dir() / "dock-tooltips" in extensions

    extensions = Style.find_extensions(template_dir(), subset=set())
    assert not extensions

    extensions = Style.find_extensions(template_dir(), subset={"advanced-docking-system"})
    assert len(extensions) == 1
    assert template_dir() / "advanced-docking-system" in extensions
