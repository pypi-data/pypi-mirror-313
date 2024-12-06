from xync_client.Abc.Auth import BaseAuthClient
from xync_schema.models import Pm

from xync_client.Abc.Ex import BaseExClient


class ExClient(BaseExClient, BaseAuthClient):
    async def curs(self) -> dict[str, str]:
        coins_curs = await self._post("/p2p/public-api/v2/currency/all-supported")
        return {c["code"]: c["code"] for c in coins_curs["data"]["fiat"]}

    async def coins(self) -> dict[str, str]:
        coins_curs = await self._post("/p2p/public-api/v2/currency/all-supported")
        return {c["code"]: c["code"] for c in coins_curs["data"]["crypto"]}

    async def _pms(self, cur: str = "RUB") -> dict[str, dict]:
        pms = await self._post("/p2p/public-api/v3/payment-details/get-methods/by-currency-code", {"currencyCode": cur})
        return {pm["code"]: {"name": pm["nameEng"]} for pm in pms["data"]}

    async def pms(self) -> dict[str, dict]:
        pms = {}
        for cur in await self.curs():
            for k, pm in (await self._pms(cur)).items():
                pms.update({k: pm})
        return pms

    async def cur_pms_map(self) -> dict[str, list[str]]:
        return {cur: list(await self._pms(cur)) for cur in await self.curs()}

    async def ads(self, coin: str, cur: str, is_sell: bool, pms: list[Pm] = None) -> list[dict]:
        params = {
            "baseCurrencyCode": coin,
            "quoteCurrencyCode": cur,
            "offerType": "SALE" if is_sell else "PURCHASE",
            "offset": 0,
            "limit": 10,
            # ,"merchantVerified":"TRUSTED"
        }
        ads = await self._post("/p2p/public-api/v2/offer/depth-of-market/", params)
        return ads
