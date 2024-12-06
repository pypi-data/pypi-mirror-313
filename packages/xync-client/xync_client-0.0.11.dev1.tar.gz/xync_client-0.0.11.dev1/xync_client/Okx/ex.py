from asyncio import run

from x_model import init_db
from xync_schema import models
from xync_schema.models import Coin, Cur, Pm, Ad, Ex

from xync_client.Abc.Base import MapOfIdsList, ListOfDicts
from xync_client.Abc.Ex import BaseExClient
from xync_client.loader import PG_DSN


class ExClient(BaseExClient):
    async def cur_pms_map(self) -> MapOfIdsList:
        pass

    async def curs(self) -> list[Cur]:
        curs = (await self._get("/v3/users/common/list/currencies"))["data"]
        return curs

    async def coins(self, cur: Cur = None) -> list[Coin]: ...

    async def pms(self, cur: Cur = None) -> ListOfDicts:
        pmcurs = {
            cur.ticker: (await self._get("/v3/c2c/configs/receipt/templates", {"quoteCurrency": cur.ticker}))["data"]
            for cur in await self.curs()
        }
        pp = {}
        [[pp.update({p["paymentMethod"]: p["paymentMethodDescription"]}) for p in ps] for ps in pmcurs.values()]
        pp = {k: v for k, v in sorted(pp.items(), key=lambda x: x[0])}
        return pp

    async def ads(self, coin: Coin, cur: Cur, is_sell: bool, pms: list[Pm] = None) -> list[Ad]:
        pass


async def main():
    _ = await init_db(PG_DSN, models, True)
    bg = await Ex.get(name="Okx")
    cl = ExClient(bg)
    # await cl.curs()
    # await cl.coins()
    await cl.pms()


run(main())
