from __future__ import annotations

import functools
import json
import warnings
from contextlib import closing
from copy import deepcopy
from xml.etree import ElementTree
from zipfile import ZipFile

from lucide._compat import open_binary
from lucide._compat import open_text
from lucide._compat import str_removeprefix


class IconDoesNotExist(Exception):
    pass


@functools.lru_cache(maxsize=1)
def _load_aliases() -> dict[str, str]:
    """Load alias mappings from aliases.json."""
    try:
        aliases_data = open_text("lucide", "aliases.json")
        with closing(aliases_data):
            return json.load(aliases_data)
    except FileNotFoundError:
        return {}


def _resolve_icon_name(name: str) -> tuple[str, bool]:
    """
    Resolve icon name, checking aliases if needed.
    Returns (resolved_name, was_alias).
    """
    aliases = _load_aliases()
    if name in aliases:
        return aliases[name], True
    return name, False


@functools.lru_cache(maxsize=128)
def _load_icon_svg(name: str) -> ElementTree.Element:
    """Load icon SVG by exact name (no alias resolution)."""
    zip_data = open_binary("lucide", "lucide.zip")
    with closing(zip_data), ZipFile(zip_data, "r") as zip_file:
        try:
            svg_bytes = zip_file.read(f"{name}.svg")
        except KeyError:
            raise IconDoesNotExist(f"The icon {name!r} does not exist.")

        svg = ElementTree.fromstring(svg_bytes.decode())
        for node in svg.iter():
            # Prevent output using the 'ns0' prefix for tags
            node.tag = ElementTree.QName(
                str_removeprefix(node.tag, "{http://www.w3.org/2000/svg}")
            )  # type: ignore[assignment]  # unclear if really allowed
        return svg


def _load_icon(name: str) -> ElementTree.Element:
    """Load icon by name, resolving aliases with deprecation warning."""
    try:
        return _load_icon_svg(name)
    except IconDoesNotExist:
        # Try alias resolution
        resolved_name, was_alias = _resolve_icon_name(name)
        if was_alias:
            warnings.warn(
                f"Icon '{name}' is deprecated, use '{resolved_name}' instead.",
                DeprecationWarning,
                stacklevel=4,  # Point to the template/caller
            )
            return _load_icon_svg(resolved_name)
        raise


_PATH_ATTR_NAMES = frozenset(
    {
        "stroke-linecap",
        "stroke-linejoin",
        "vector-effect",
    }
)


def _render_icon(name: str, size: int | None, **kwargs: object) -> str:
    svg = deepcopy(_load_icon(name))
    if size is not None:
        svg.attrib["width"] = svg.attrib["height"] = str(size)

    svg_attrs = {}
    path_attrs = {}
    for raw_name, value in kwargs.items():
        attr_name = raw_name.replace("_", "-")
        if attr_name in _PATH_ATTR_NAMES:
            path_attrs[attr_name] = str(value)
        else:
            svg_attrs[attr_name] = str(value)

    svg.attrib.update(svg_attrs)
    if path_attrs:
        for path in svg.findall("path"):
            path.attrib.update(path_attrs)

    string = ElementTree.tostring(svg, encoding="unicode")
    # Inline SVG's don't need xmlns
    return string.replace(' xmlns="http://www.w3.org/2000/svg"', "", 1)
