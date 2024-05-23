# Hightop.py

A nice shortcut for group count queries with Django

```python
Visit.objects.top('browser')
# {
#   'Chrome': 63,
#   'Safari': 50,
#   'Firefox': 34
# }
```

[![Build Status](https://github.com/ankane/hightop.py/actions/workflows/build.yml/badge.svg)](https://github.com/ankane/hightop.py/actions)

## Installation

Run:

```sh
pip install hightop
```

## Getting Started

Add a [custom manager](https://docs.djangoproject.com/en/3.2/topics/db/managers/) to the models where you want to use it.

```python
from hightop import HightopQuerySet

class Visit(models.Model):
    objects = HightopQuerySet.as_manager()
```

And query away

```python
Visit.objects.top('browser')
```

## Options

Limit the results

```python
Visit.objects.top('referring_domain', 10)
```

Include null values

```python
Visit.objects.top('search_keyword', null=True)
```

Works with multiple groups

```python
Visit.objects.top(['city', 'browser'])
```

And expressions

```python
Visit.objects.top(Lower('referring_domain'))
```

And distinct

```python
Visit.objects.top('city', distinct='user_id')
```

And min count

```python
Visit.objects.top('city', min=10)
```

## History

View the [changelog](https://github.com/ankane/hightop.py/blob/master/CHANGELOG.md)

## Contributing

Everyone is encouraged to help improve this project. Here are a few ways you can help:

- [Report bugs](https://github.com/ankane/hightop.py/issues)
- Fix bugs and [submit pull requests](https://github.com/ankane/hightop.py/pulls)
- Write, clarify, or fix documentation
- Suggest or add new features

To get started with development:

```sh
git clone https://github.com/ankane/hightop.py.git
cd hightop.py
pip install -r requirements.txt
pytest
```
