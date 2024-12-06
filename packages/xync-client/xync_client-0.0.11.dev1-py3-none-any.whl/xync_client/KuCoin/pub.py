from asyncio import run

from x_model import init_db
from xync_schema import models
from xync_schema.models import Coin, Cur, Pm, Ad, Ex, Curex

from xync_client.Abc.Base import MapOfIdsList
from xync_client.Abc.Ex import BaseExClient
from xync_client.loader import PG_DSN


class ExClient(BaseExClient):
    async def cur_pms_map(self) -> MapOfIdsList:
        pass

    async def curs(self) -> list[Cur]:
        curs = (await self._get("/_api/otc/dictionary/getData", {"type": "LEGAL"}))["data"]
        curs = [(await Cur.update_or_create(ticker=cur["typeCode"]))[0] for cur in curs]
        curexs = [Curex(cur=c, ex=self.ex) for c in curs]
        await Curex.bulk_create(curexs, ignore_conflicts=True)
        return curs

    async def coins(self, cur: Cur = None) -> list[Coin]: ...

    async def pms(self, cur: Cur = None) -> list[Pm]:
        pmcurs = {
            cur.ticker: (await self._get("/_api/otc/legal/payTypes", {"legal": cur.ticker}))["data"]
            for cur in await self.curs()
        }
        pp = {}
        [[pp.update({p["payTypeCode"]: p["payTypeName"]}) for p in ps] for ps in pmcurs.values()]
        return pp

    async def ads(self, coin: Coin, cur: Cur, is_sell: bool, pms: list[Pm] = None) -> list[Ad]:
        pass


async def main():
    _ = await init_db(PG_DSN, models, True)
    bg = await Ex.get(name="KuCoin")
    cl = ExClient(bg)
    # await cl.curs()
    # await cl.coins()
    await cl.pms()


run(main())
