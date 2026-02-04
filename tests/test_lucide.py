from __future__ import annotations

from xml.etree import ElementTree

import pytest

import lucide


def test_load_icon_success_outline():
    svg = lucide._load_icon("a-arrow-down")
    assert isinstance(svg, ElementTree.Element)
    assert svg.tag == ElementTree.QName("svg")


def test_load_icon_success_solid():
    svg = lucide._load_icon("a-arrow-down")
    assert isinstance(svg, ElementTree.Element)
    assert svg.tag == ElementTree.QName("svg")


def test_load_icon_success_mini():
    svg = lucide._load_icon("a-arrow-down")
    assert isinstance(svg, ElementTree.Element)
    assert svg.tag == ElementTree.QName("svg")


def test_load_icon_fail_unknown():
    with pytest.raises(lucide.IconDoesNotExist) as excinfo:
        lucide._load_icon("hoome")

    assert excinfo.value.args == ("The icon 'hoome' does not exist.",)


def test_load_icon_alias_resolves():
    """Test that deprecated alias 'edit-2' resolves to 'pen'."""
    import warnings

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        svg = lucide._load_icon("edit-2")

        assert isinstance(svg, ElementTree.Element)
        assert svg.tag == ElementTree.QName("svg")

        # Check deprecation warning was raised
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "edit-2" in str(w[0].message)
        assert "pen" in str(w[0].message)


def test_load_icon_alias_same_as_target():
    """Test that alias returns same SVG as target icon."""
    import warnings

    # Load via alias (suppress warning)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        svg_alias = lucide._render_icon("edit-2", size=24)

    # Load directly
    svg_direct = lucide._render_icon("pen", size=24)

    assert svg_alias == svg_direct
