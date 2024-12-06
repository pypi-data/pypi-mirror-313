from x_client.aiohttp import Client
from xync_schema.models import Ex

DictOfDicts = dict[int | str, dict]
ListOfDicts = list[dict]
FlatDict = dict[int | str, str]
MapOfIdsList = dict[int | str, list[int | str]]


class BaseClient(Client):
    def __init__(self, ex: Ex):
        super().__init__(ex.host_p2p)
