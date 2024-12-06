Wilhelm Data Loader
===================

![Python Version][Python Version Badge]
[![Read the Docs][Read the Docs badge]][Read the Docs URL]
[![PyPI][PyPI project badge]][PyPI project url]
[![GitHub Workflow Status][GitHub Workflow Status badge]][GitHub Workflow Status URL]
[![Apache License badge]][Apache License URL]

Wilhelm Data Loader is a data pipeline that reads  [Wilhelm](https://wilhelmlang.com/)'s vocabulary data from supported
data sources and loads them into graph databases

Some features can be reused as SDK which can be installed via

```console
pip install wilhelm_data_loader
```

Details documentations can be found at [sdk.wilhelmlang.com](https://sdk.wilhelmlang.com/)

Development
-----------

### Environment Setup

Get the source code:

```console
git clone git@github.com:QubitPi/wilhelm-data-loader.git
cd wilhelm-data-loader
```

It is strongly recommended to work in an isolated environment. Install virtualenv and create an isolated Python
environment by

```console
python3 -m pip install --user -U virtualenv
python3 -m virtualenv .venv
```

To activate this environment:

```console
source .venv/bin/activate
```

or, on Windows

```console
./venv\Scripts\activate
```

> [!TIP]
>
> To deactivate this environment, use
>
> ```console
> deactivate
> ```

### Installing Dependencies

```console
pip3 install -r requirements.txt
```

License
-------

The use and distribution terms for [Wilhelm Graph Database Python SDK]() are covered by the
[Apache License, Version 2.0].

[Apache License badge]: https://img.shields.io/badge/Apache%202.0-F25910.svg?style=for-the-badge&logo=Apache&logoColor=white
[Apache License URL]: https://www.apache.org/licenses/LICENSE-2.0
[Apache License, Version 2.0]: http://www.apache.org/licenses/LICENSE-2.0.html

[GitHub Workflow Status badge]: https://img.shields.io/github/actions/workflow/status/QubitPi/wilhelm-python-sdk/ci-cd.yml?logo=github&style=for-the-badge&label=CI/CD
[GitHub Workflow Status URL]: https://github.com/QubitPi/wilhelm-python-sdk/actions/workflows/ci-cd.yml

[Python Version Badge]: https://img.shields.io/badge/Python-3.10-brightgreen?style=for-the-badge&logo=python&logoColor=white
[PyPI project badge]: https://img.shields.io/pypi/v/wilhelm-python-sdk?logo=pypi&logoColor=white&style=for-the-badge
[PyPI project url]: https://pypi.org/project/wilhelm-python-sdk/

[Read the Docs badge]: https://img.shields.io/readthedocs/wilhelm-python-sdk?style=for-the-badge&logo=readthedocs&logoColor=white&label=Read%20the%20Docs&labelColor=8CA1AF
[Read the Docs URL]: https://sdk.wilhelmlang.com
