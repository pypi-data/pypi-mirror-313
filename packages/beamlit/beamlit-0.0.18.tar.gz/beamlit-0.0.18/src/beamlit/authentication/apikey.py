from typing import Generator

from httpx import Auth, Request, Response


class ApiKeyProvider(Auth):
    def __init__(self, credentials, workspace_name: str):
        self.credentials = credentials
        self.workspace_name = workspace_name

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        request.headers['X-Beamlit-Api-Key'] = self.credentials.api_key
        request.headers['X-Beamlit-Workspace'] = self.workspace_name
        yield request
