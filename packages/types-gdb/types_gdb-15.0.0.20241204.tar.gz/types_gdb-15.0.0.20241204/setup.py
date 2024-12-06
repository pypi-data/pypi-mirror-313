from setuptools import setup

name = "types-gdb"
description = "Typing stubs for gdb"
long_description = '''
## Typing stubs for gdb

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`gdb`](https://sourceware.org/git/gitweb.cgi?p=binutils-gdb.git;a=tree) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `gdb`. This version of
`types-gdb` aims to provide accurate annotations for
`gdb==15.0.*`.

Type hints for GDB's [Python API](https://sourceware.org/gdb/onlinedocs/gdb/Python-API.html). Note that this API is available only when running Python scripts under GDB: it is not possible to install the `gdb` package separately, for instance using `pip`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/gdb`](https://github.com/python/typeshed/tree/main/stubs/gdb)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`7fbb5fe32ba3d92ba51d9e06837b48895cf5f038`](https://github.com/python/typeshed/commit/7fbb5fe32ba3d92ba51d9e06837b48895cf5f038).
'''.lstrip()

setup(name=name,
      version="15.0.0.20241204",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/gdb.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['gdb-stubs'],
      package_data={'gdb-stubs': ['FrameDecorator.pyi', 'FrameIterator.pyi', '__init__.pyi', 'dap/__init__.pyi', 'dap/breakpoint.pyi', 'dap/bt.pyi', 'dap/disassemble.pyi', 'dap/evaluate.pyi', 'dap/events.pyi', 'dap/frames.pyi', 'dap/io.pyi', 'dap/launch.pyi', 'dap/locations.pyi', 'dap/memory.pyi', 'dap/modules.pyi', 'dap/next.pyi', 'dap/pause.pyi', 'dap/scopes.pyi', 'dap/server.pyi', 'dap/sources.pyi', 'dap/startup.pyi', 'dap/state.pyi', 'dap/threads.pyi', 'dap/typecheck.pyi', 'dap/varref.pyi', 'disassembler.pyi', 'events.pyi', 'missing_debug.pyi', 'printing.pyi', 'prompt.pyi', 'types.pyi', 'unwinder.pyi', 'xmethod.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
