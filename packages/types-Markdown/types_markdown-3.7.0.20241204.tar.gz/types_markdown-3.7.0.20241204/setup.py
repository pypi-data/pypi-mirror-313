from setuptools import setup

name = "types-Markdown"
description = "Typing stubs for Markdown"
long_description = '''
## Typing stubs for Markdown

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`Markdown`](https://github.com/Python-Markdown/markdown) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `Markdown`. This version of
`types-Markdown` aims to provide accurate annotations for
`Markdown==3.7.*`.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/Markdown`](https://github.com/python/typeshed/tree/main/stubs/Markdown)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`7fbb5fe32ba3d92ba51d9e06837b48895cf5f038`](https://github.com/python/typeshed/commit/7fbb5fe32ba3d92ba51d9e06837b48895cf5f038).
'''.lstrip()

setup(name=name,
      version="3.7.0.20241204",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Markdown.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['markdown-stubs'],
      package_data={'markdown-stubs': ['__init__.pyi', '__meta__.pyi', 'blockparser.pyi', 'blockprocessors.pyi', 'core.pyi', 'extensions/__init__.pyi', 'extensions/abbr.pyi', 'extensions/admonition.pyi', 'extensions/attr_list.pyi', 'extensions/codehilite.pyi', 'extensions/def_list.pyi', 'extensions/extra.pyi', 'extensions/fenced_code.pyi', 'extensions/footnotes.pyi', 'extensions/legacy_attrs.pyi', 'extensions/legacy_em.pyi', 'extensions/md_in_html.pyi', 'extensions/meta.pyi', 'extensions/nl2br.pyi', 'extensions/sane_lists.pyi', 'extensions/smarty.pyi', 'extensions/tables.pyi', 'extensions/toc.pyi', 'extensions/wikilinks.pyi', 'inlinepatterns.pyi', 'postprocessors.pyi', 'preprocessors.pyi', 'serializers.pyi', 'treeprocessors.pyi', 'util.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
