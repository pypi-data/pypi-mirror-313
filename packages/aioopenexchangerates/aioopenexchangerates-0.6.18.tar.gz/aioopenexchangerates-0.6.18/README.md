# aioopenexchangerates

<p align="center">
  <a href="https://github.com/MartinHjelmare/aioopenexchangerates/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/MartinHjelmare/aioopenexchangerates/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://aioopenexchangerates.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/aioopenexchangerates.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
  <a href="https://codecov.io/gh/MartinHjelmare/aioopenexchangerates">
    <img src="https://img.shields.io/codecov/c/github/MartinHjelmare/aioopenexchangerates.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json" alt="Poetry">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/aioopenexchangerates/">
    <img src="https://img.shields.io/pypi/v/aioopenexchangerates.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/aioopenexchangerates.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/aioopenexchangerates.svg?style=flat-square" alt="License">
</p>

---

**Documentation**: <a href="https://aioopenexchangerates.readthedocs.io" target="_blank">https://aioopenexchangerates.readthedocs.io </a>

**Source Code**: <a href="https://github.com/MartinHjelmare/aioopenexchangerates" target="_blank">https://github.com/MartinHjelmare/aioopenexchangerates </a>

---

Fetch rates from openexchangerates with aiohttp.

## Installation

Install this via pip (or your favourite package manager):

`pip install aioopenexchangerates`

## Usage

```py
import asyncio

from aioopenexchangerates import Client, OpenExchangeRatesError


async def main() -> None:
    """Run main."""
    async with Client("your_api_key") as client:
        try:
            result = await client.get_latest()
        except OpenExchangeRatesError as err:
            print(err)
        else:
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

## Credits

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
