from __future__ import annotations

from typing import Any

import django
from django.conf import settings
from django.template import Context
from django.template import Template

settings.configure(
    ROOT_URLCONF=__name__,  # Make this module the urlconf
    SECRET_KEY="insecure",
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": False,
        },
    ],
    INSTALLED_APPS=["lucide"],
)
urlpatterns: list[Any] = []
django.setup()


def test_success_icon():
    template = Template('{% load lucide %}{% lucide "a-arrow-down" %}')

    result = template.render(Context())
    print(result)
    assert result == (
        # fmt: off
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n  <path d="m14 12 4 4 4-4" />\n  <path d="M18 16V7" />\n  <path d="m2 16 4.039-9.69a.5.5 0 0 1 .923 0L11 16" />\n  <path d="M3.304 13h6.392" />\n</svg>'
        # fmt: on
    )


def test_success_icon_path_attr():
    template = Template(
        "{% load lucide %}" + '{% lucide "a-arrow-down" stroke_linecap="butt" %}'
    )

    result = template.render(Context())

    assert result == (
        # fmt: off
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n  <path d="m14 12 4 4 4-4" stroke-linecap="butt" />\n  <path d="M18 16V7" stroke-linecap="butt" />\n  <path d="m2 16 4.039-9.69a.5.5 0 0 1 .923 0L11 16" stroke-linecap="butt" />\n  <path d="M3.304 13h6.392" stroke-linecap="butt" />\n</svg>'
        # fmt: on
    )


def test_success_icon_complete():
    template = Template(
        "{% load lucide %}"
        + '{% lucide "a-arrow-down" size=48 class="h-4 w-4" '
        + 'data_test="a < 2" %}'
    )

    result = template.render(Context())

    assert result == (
        # fmt: off
        '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" data-test="a &lt; 2">\n  <path d="m14 12 4 4 4-4" />\n  <path d="M18 16V7" />\n  <path d="m2 16 4.039-9.69a.5.5 0 0 1 .923 0L11 16" />\n  <path d="M3.304 13h6.392" />\n</svg>'
        # fmt: on
    )


def test_success_icon_size_none():
    template = Template("{% load lucide %}" + '{% lucide "a-arrow-down" size=None %}')

    result = template.render(Context())

    assert result == (
        # fmt: off
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n  <path d="m14 12 4 4 4-4" />\n  <path d="M18 16V7" />\n  <path d="m2 16 4.039-9.69a.5.5 0 0 1 .923 0L11 16" />\n  <path d="M3.304 13h6.392" />\n</svg>'
        # fmt: on
    )


def test_dynamic_template_attribute():
    """Test that template variables in attributes are rendered."""
    template = Template(
        '{% load lucide %}{% lucide "a-arrow-down" class="{{ my_class }}" %}'
    )

    result = template.render(Context({"my_class": "icon-large"}))

    assert 'class="icon-large"' in result


def test_dynamic_template_attribute_multiple():
    """Test multiple dynamic attributes."""
    template = Template(
        '{% load lucide %}{% lucide "a-arrow-down" class="{{ cls }}" data_id="{{ id }}" %}'
    )

    result = template.render(Context({"cls": "my-icon", "id": "123"}))

    assert 'class="my-icon"' in result
    assert 'data-id="123"' in result


def test_malformed_template_syntax_fallback():
    """Test that malformed template syntax falls back to original string."""
    from lucide.templatetags.lucide import _render_icon
    from django.template import Context

    # Directly call _render_icon with malformed template syntax
    # {% invalid_tag %} triggers TemplateSyntaxError
    result = _render_icon(
        Context(),
        "a-arrow-down",
        24,
        data_info="{% invalid_tag %}"  # Invalid tag triggers TemplateSyntaxError
    )

    # Should contain the original malformed string as fallback
    assert "{% invalid_tag %}" in result
