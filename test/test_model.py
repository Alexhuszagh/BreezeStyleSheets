import pytest

from breezestylesheets import model


@pytest.mark.parametrize(
    "input,expected",
    [
        (
            "foreground",
            (
                "fg",
                "fg-default",
                "fg.default",
                "fg:default",
                "foreground",
                "foreground-default",
                "foreground.default",
                "foreground:default",
            ),
        ),
        (
            "foreground.light",
            (
                "fg-light",
                "fg.light",
                "fg:light",
                "foreground-light",
                "foreground.light",
                "foreground:light",
            ),
        ),
        (
            "foreground:light",
            (
                "fg-light",
                "fg.light",
                "fg:light",
                "foreground-light",
                "foreground.light",
                "foreground:light",
            ),
        ),
        (
            "toolbar:horizontal:background",
            (
                "toolbar-horizontal-background",
                "toolbar-horizontal-bg",
                "toolbar.horizontal.background",
                "toolbar.horizontal.bg",
                "toolbar:horizontal:background",
                "toolbar:horizontal:bg",
            ),
        ),
    ],
)
def test_expand_aliases(input: "str", expected: "model.Alias") -> "None":
    assert expected == model.expand_aliases(input)
