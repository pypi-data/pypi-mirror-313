import logging

from aiohttp import ClientResponse
from aiohttp.http_exceptions import HttpProcessingError
from x_client.http import Client as HttpClient
from xync_client.Abc.Auth import BaseAuthClient
from xync_schema.models import Agent

from xync_client.TgWallet.pyro import PyroClient


class AuthClient(BaseAuthClient):
    def __init__(self, agent: Agent):
        self.meth = {
            "GET": self._get,
            "POST": self._post,
            "DELETE": self._delete,
        }
        super().__init__(agent)

    async def _get_auth_hdrs(self) -> dict[str, str]:
        pyro = PyroClient(self.agent)
        init_data = await pyro.get_init_data()
        tokens = HttpClient("walletbot.me")._post("/api/v1/users/auth/", init_data)
        return {"Wallet-Authorization": tokens["jwt"], "Authorization": "Bearer " + tokens["value"]}

    async def login(self) -> None:
        auth_hdrs: dict[str, str] = await self._get_auth_hdrs()
        self.session.headers.update(auth_hdrs)

    async def _proc(self, resp: ClientResponse, data: dict = None) -> dict | str:
        try:
            return await super()._proc(resp)
        except HttpProcessingError as e:
            if e.code == 401:
                logging.warning(e)
                await self.login()
                res = await self.meth[resp.method](resp.url.path, data)
                return res
