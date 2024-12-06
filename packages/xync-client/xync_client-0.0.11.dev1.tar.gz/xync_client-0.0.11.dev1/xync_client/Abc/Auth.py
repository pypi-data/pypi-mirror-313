from xync_client.Abc.Base import BaseClient
from xync_schema.models import Agent


class BaseAuthClient(BaseClient):
    def __init__(self, agent: Agent):
        self.headers.update(agent.auth)
        self.agent = agent
        super().__init__(agent.ex)
