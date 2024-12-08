[![PyPI](https://img.shields.io/pypi/v/bytewax-webflow.svg?style=flat-square)](https://pypi.org/project/bytewax-webflow/)


# Bytewax Webflow

[Webflow](https://webflow.com/) connectors for [Bytewax](https://bytewax.io).

This connector offers 1 sink:

* `WebflowCollectionItemSink` - inserts or updates a specified Webflow Collection.

## Installation

This package is available via [PyPi](https://pypi.org/project/bytewax-webflow) as
`bytewax-webflow` and can be installed via your package manager of choice.

## Usage

```python
import os

import bytewax.operators as op
from bytewax.testing import TestingSource
from bytewax.dataflow import Dataflow

from bytewax_webflow import CollectionItemSink, CollectionItem

WEBFLOW_ACCESS_TOKEN = os.environ["WEBFLOW_ACCESS_TOKEN"]
WEBFLOW_COLLECTION_ID = os.environ["WEBFLOW_COLLECTION_ID"]

flow = Dataflow("webflow_example")

flow_input = op.input("input", flow, TestingSource(["Earth", "Mars"]))


def create_webflow_item(value: str) -> CollectionItem:
    return CollectionItem(
        name=f"Hello {value}",
        slug=value,
        fields={
            "planet": value,
        }
    )

transform = op.map("transform", flow_input, create_webflow_item)

op.output("output", transform, CollectionItemSink(WEBFLOW_ACCESS_TOKEN, WEBFLOW_COLLECTION_ID))
```

## License

Licensed under the [MIT License](./LICENSE).
