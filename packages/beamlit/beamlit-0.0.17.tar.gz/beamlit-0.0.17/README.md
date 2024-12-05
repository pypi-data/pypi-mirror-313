# beamlit
A client library for accessing Beamlit Control Plane

## Usage
First, create a client:

```python
from beamlit.authentication import (RunClientWithCredentials, load_credentials,
                                    new_client_with_credentials)

WORKSPACE_NAME = "development"
credentials = load_credentials(WORKSPACE_NAME)
config = RunClientWithCredentials(
    credentials=credentials,
    workspace=WORKSPACE_NAME,
)
client = new_client_with_credentials(config)
```

Now call your endpoint and use your models:

```python
from typing import List

from beamlit.api.models import list_models
from beamlit.types import Response
from beamlit.models.model import Model

with client as client:
    models: List[Model] = list_models.sync(client=client)
    # or if you need more info (e.g. status_code)
    response: Response[List[Model]] = list_models.sync_detailed(client=client)
```

Or do the same thing with an async version:

```python
from typing import List

from beamlit.api.models import list_models
from beamlit.types import Response
from beamlit.models.model import Model

async with client as client:
    models: List[Model] = await list_models.asyncio(client=client)
    response: Response[List[Model]] = await list_models.asyncio_detailed(client=client)
```