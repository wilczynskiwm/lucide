# lucide

Use [Lucide icons](https://lucide.dev/) in your Django and Jinja templates.

> **Fork of [franciscobmacedo/lucide](https://github.com/franciscobmacedo/lucide)** with additional features:
> - Dynamic template attribute rendering (use `{{ variables }}` in attributes)
> - Icon alias support with deprecation warnings (246 aliases)
> - Automatic icon updates via GitHub Actions

## Requirements

Python 3.8 to 3.12 supported.

Django 3.2 to 5.0 supported.

## Installation

```bash
pip install lucide
```

## Usage

The `lucide` package supports both Django templates and Jinja templates.

### Django templates

1. Add to your `INSTALLED_APPS`:

    ```python
    INSTALLED_APPS = [
        ...,
        "lucide",
        ...,
    ]
    ```

2. Load the template library:

    ```django
    {% load lucide %}
    ```

3. Use icons:

    ```django
    {% lucide "arrow-down" %}
    {% lucide "arrow-down" size=40 class="mr-4" %}
    {% lucide "arrow-down" stroke_width=1 data_controller="icon" %}
    ```

#### Dynamic attributes

You can use template variables in attributes:

```django
{% lucide "user" class="{{ css_class }}" data-id="{{ user.id }}" %}
```

#### Icon aliases

Old icon names automatically resolve to new names with a deprecation warning:

```django
{% lucide "edit-2" %}  {# Works, but warns to use "pen" instead #}
```

### Jinja templates

1. Add the global function to your environment:

    ```python
    from lucide.jinja import lucide
    from jinja2 import Environment

    env = Environment()
    env.globals.update({"lucide": lucide})
    ```

2. Use icons:

    ```jinja
    {{ lucide("arrow-down") }}
    {{ lucide("arrow-down", size=40, class="mr-4") }}
    ```

## Icon reference

Browse all available icons at [lucide.dev/icons](https://lucide.dev/icons/).

## Acknowledgements

- Original package by [franciscobmacedo](https://github.com/franciscobmacedo/lucide)
- Inspired by [Adam Johnson's heroicons](https://github.com/adamchainz/heroicons)
