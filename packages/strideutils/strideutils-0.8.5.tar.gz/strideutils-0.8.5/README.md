## Description

Strideutils contains common patterns for cosmos api requests, monitoring, and other integrations for gsheets, slack, and twilio.

## Setup

In a virtual environment of your choice install strideutils.

```
pip install strideutils
```

with poetry

```
poetry add strideutils
```

This package is frequently updated, so keep that in mind while developing.

## Configuration

Strideutils requires three different environment variables that can be added to `~/.zshrc` or `~/.bashrc`

```
export STRIDEUTILS_CONFIG_PATH=
export STRIDEUTILS_ENV_PATH=
```

Examples of these files are included under strideutils/config_examples.
Stride Labs employees can find config.yaml in launchpad and .env.local in lastpass. We recommend you place .env.local in your launchpad repo.

Any configuration or secrets that aren't consumed don't need to be set. However if one is accessed but unset, an error will be thrown for easier debugging.

Once strideutils is installed and configured, each module you need should be imported individually. This isolates the different secrets that are expected and consumed.

Some common imports:

```python
from strideutils.stride_config import config
config.get_chain(name='osmosis')

from strideutils import stride_requests
stride_requests.request('https://google.com')

from strideutils.stride_alerts import raise_alert
```

## Slack Connector

TODO

## Sheets Connector

TODO

## Redis Connector

TODO

## Developing Strideutils

To access the strideutils repo locally rather than using the pip version (for actively making changes to strideutils and a dependency), add the path to strideutils to the beginning of PYTHONPATH

```python
import sys
sys.path = ['/path/to/strideutils/'] + sys.path
```

Alternatively, you can install strideutils through local mode. However, please be warned that this will make your local Python environment _always_ use your local strideutils. This might lead to unexpected behavior if you local changes.

To install in local mode, run the following:

```python
pip3 install -e /Users/username/Documents/strideutils
```

Confirm the location of where it's being imported from by printing the module.
After making changes to strideutils, reload it before testing your application.

```python
from importlib import reload
reload(strideutils)
```
