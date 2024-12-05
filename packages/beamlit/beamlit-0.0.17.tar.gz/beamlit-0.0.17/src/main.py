from typing import List

from beamlit.api.models import list_models
from beamlit.authentication import (RunClientWithCredentials, load_credentials,
                                    new_client_with_credentials)
from beamlit.models.model import Model

credentials = load_credentials("development")
config = RunClientWithCredentials(
    credentials=credentials,
    workspace="development",
)
client = new_client_with_credentials(config)

with client as client:
    models: List[Model] = list_models.sync(client=client)
    print(models)
    print(models)
