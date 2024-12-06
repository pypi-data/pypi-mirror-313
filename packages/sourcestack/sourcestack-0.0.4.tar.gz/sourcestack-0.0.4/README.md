# SourceStack

[![LICENSE](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/workflowing/sourcestack/blob/main/LICENSE)
[![PyPi](https://img.shields.io/pypi/v/sourcestack)](https://pypi.org/project/sourcestack/)
[![GitHub](https://img.shields.io/badge/github-repo-blue.svg)](https://github.com/workflowing/sourcestack)

## Installation

```bash
pip install sourcestack
```

## Usage

```python
from sourcestack.client import Client

client = Client(api_key="fake-api-key")
client.session
```

## Building

```bash
pip install setuptools
```

```bash
bin/build
```

## Publishing

```bash
pip install twine
```

```bash
bin/publish
```
