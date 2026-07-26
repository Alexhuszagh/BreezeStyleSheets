"""Miscellaneous utilities when working with XML."""

_ESCAPE = str.maketrans({
    "<": "&lt;",
    ">": "&gt;",
    "&": "&amp;",
    "'": "&apos;",
    '"': "&quot;",
})


def xml_escape(value: "str") -> "str":
    """Safely escape XML characters for direct inclusion in an XML entity."""
    return value.translate(_ESCAPE)
