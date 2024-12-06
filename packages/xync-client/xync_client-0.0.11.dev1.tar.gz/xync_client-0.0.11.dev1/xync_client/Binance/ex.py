from xync_schema.enums import PmType

from xync_client.Abc.Ex import BaseClient
from xync_client.Binance.sapi import Sapi
from xync_schema.models import Ex


class Client(BaseClient):
    def __init__(self, ex: Ex, bkeys):
        self.sapi = Sapi(*bkeys)
        super().__init__(ex)

    async def curs(self) -> dict:
        curs = await self._post("/bapi/c2c/v1/friendly/c2c/trade-rule/fiat-list")
        return {c["currencyCode"]: c["countryCode"] for c in curs["data"]}

    async def coins(self) -> list[dict]:
        pass

    async def pms(self) -> dict[str, dict]:
        pms = await self.sapi.get_pay_meths()
        return {
            pm["id"]: {
                "name": pm["name"],
                "identifier": pm["identifier"],
                "type_": PmType[pm["typeCode"].replace("-", "_")].value,
                "logo": pm["iconUrlColor"],
            }
            for pm in pms["data"]
        }

    # 22: Cur -> [Pm] rels
    async def cur_pms_map(self) -> dict[int, set[int]]:  # {cur.exid: [pm.exid], [pm.exid]}
        res = await self.curs()
        mp = {c: await self._get_pms_for_cur(c) for c in res.keys()}
        return mp

    # # 22: Cur -> [Pm] rels
    # async def cur_countries_map(self) -> dict[int, set[int]]:  # {cur.exid: [pm.exid]}
    #     res = await self._get_pms_and_country_for_cur()
    #     wrong_pms = {4, 34, 212, 239, 363, 498, 548, 20009, 20010}  # these ids not exist in pms
    #     return {c['currencyId']: set(c['supportPayments']) - wrong_pms for c in res['currency'] if c["supportPayments"]}

    async def ads(self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str] = None) -> list[dict]:
        pass

    async def _get_pms_for_cur(self, cur: str) -> ([str], [str]):
        data = {"fiat": cur, "classifies": ["mass", "profession"]}
        res = await self._post("/bapi/c2c/v2/public/c2c/adv/filter-conditions", data)
        return [r["identifier"] for r in res["data"]["tradeMethods"]]
        # , [
        #     r["scode"] for r in res["data"]["countries"] if r["scode"] != "ALL"
        # ]  # countries,tradeMethods,periods


# class Private(Public): # todo: base class: Public or Client?
# class Private(Client):
#     # auth: dict =
#     headers: dict = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
#         "Content-Type": "application/json",
#         "clienttype": "web",
#     }
#
#     def seq_headers(self):
#         return {
#             "csrftoken": self.auth["tok"],
#             "cookie": f'p20t=web.{self.id}.{self.auth["cook"]}',
#         }


# async def main():
#     _ = await init_db(PG_DSN, models, True)
#     ex = await Ex.get(name="Binance")
#     cl = Client(ex, (BKEY, BSEC))
#     await cl.set_pmcurexs()
#     await cl.close()
#
#
# run(main())
