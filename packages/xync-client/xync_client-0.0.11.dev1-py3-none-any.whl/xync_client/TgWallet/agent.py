from enum import StrEnum, IntEnum
from typing import Literal

from x_client.http import Client as HttpClient
from xync_schema.models import User, Cur, Order, Coin, OrderStatus, Pmex
from xync_schema.pydantic import FiatNew

from xync_client.Abc.Agent import BaseAgentClient
from xync_client.TgWallet.pyro import PyroClient


class Exceptions(StrEnum):
    PM_KYC = "OFFER_FIAT_COUNTRY_NOT_SUPPORTED_BY_USER_KYC_COUNTRY"


class Status(IntEnum):
    ALL_ACTIVE = OrderStatus.active


class AgentClient(BaseAgentClient):
    async def order_request(self, ad_id: int, amount: float) -> Order:
        pass

    async def _get_auth_hdrs(self) -> dict[str, str]:
        pyro = PyroClient(self.agent)
        init_data = await pyro.get_init_data()
        tokens = HttpClient("walletbot.me")._post("/api/v1/users/auth/", init_data)
        return {"Wallet-Authorization": tokens["jwt"], "Authorization": "Bearer " + tokens["value"]}

    async def get_orders(
        self, stauts: OrderStatus = OrderStatus.active, coin: Coin = None, cur: Cur = None, is_sell: bool = None
    ) -> list[Order]:
        orders = await self._post(
            "/p2p/public-api/v2/offer/order/history/get-by-user-id",
            {"offset": 0, "limit": 100, "filter": {"status": Status(stauts)}},  # "limit": 20
        )
        return orders

    async def my_fiats(self, cur: Cur = None) -> dict:
        fiats = await self._post("/p2p/public-api/v3/payment-details/get/by-user-id")
        fiats = {fiat["id"]: fiat for fiat in fiats["data"]}
        return fiats

    async def fiat_new(self, fiat: FiatNew):
        pmex = await Pmex.get_or_create(pm_id=fiat.pm_id, ex=self.agent.ex)  # .prefetch_related('pm')
        cur = await Cur[fiat.cur_id]
        add_fiat = await self._post(
            "/p2p/public-api/v3/payment-details/create",
            {
                "paymentMethodCode": pmex.exid,
                "currencyCode": cur.ticker,
                "name": fiat.name,
                "attributes": {"version": "V1", "values": [{"name": "PAYMENT_DETAILS_NUMBER", "value": fiat.detail}]},
            },
        )
        return add_fiat

    # 7 - fiat_edit
    async def fiat_upd(self, fiat_id: int, name: str, detail: str):
        edit_fiat = await self._post(
            "/p2p/public-api/v3/payment-details/edit",
            {
                "id": fiat_id,
                # "paymentMethodCode": code_pms,
                # "currencyCode": cur,
                "name": name,
                "attributes": {"version": "V1", "values": [{"name": "PAYMENT_DETAILS_NUMBER", "value": detail}]},
            },
        )
        return edit_fiat

    async def fiat_del(self, fiat_id: int):
        del_fiat = await self._post("/p2p/public-api/v3/payment-details/delete", {"id": fiat_id})
        return del_fiat

    async def ad_switch(self) -> bool:
        pass

    async def ads_switch(self) -> bool:
        pass

    async def get_user(self, user_id) -> User:
        pass

    async def send_user_msg(self, msg: str, file=None) -> bool:
        pass

    async def block_user(self, is_blocked: bool = True) -> bool:
        pass

    async def rate_user(self, positive: bool) -> bool:
        pass

    # base_url = 'https://p2p.walletbot.me'
    # middle_url = '/p2p/'

    # 1: all_curs
    async def all_curs(self):
        coins_curs = await self._post("/p2p/public-api/v2/currency/all-supported")
        curs = [c["code"] for c in coins_curs["data"]["fiat"]]
        return curs

    # 2: all_coins
    async def all_coins(self):
        coins_curs = await self._post("/p2p/public-api/v2/currency/all-supported")
        coins = [c["code"] for c in coins_curs["data"]["crypto"]]
        return coins

    # 3: all_coins
    async def all_pms(self):
        pms = await self._post(
            "/p2p/public-api/v3/payment-details/get-methods/by-currency-code", {"currencyCode": "RUB"}
        )
        return pms["data"]

    # 4: all_ads
    async def get_ads(
        self, coin: str = "TON", cur: str = "RUB", tt: str = "SALE", offset: int = 0, limit: int = 100
    ) -> dict:
        params = {
            "baseCurrencyCode": coin,
            "quoteCurrencyCode": cur,
            "offerType": tt,
            "offset": offset,
            "limit": limit,
        }  # ,"merchantVerified":"TRUSTED"
        ads = await self._post("/p2p/public-api/v2/offer/depth-of-market/", params)
        return ads

    # 6: cancel_order
    async def cancel_order(self, orderId: int):
        data = {"orderId": orderId}
        cancel = await self._post("/p2p/public-api/v2/offer/order/cancel/by-buyer", json=data)
        return cancel

    # 9 - my_ads
    async def my_ads(self, status: Literal["INACTIVE", "ACTIVE"] = None):
        ads = await self._post(
            "/p2p/public-api/v2/offer/user-own/list", {"offset": 0, "limit": 20, "offerType": "SALE"}
        )
        return [ad for ad in ads["data"] if ad["status"] == status] if status else ads

    # 10 - ad_new
    async def ad_new(self, fiats: list[int], amount: int, coin: str = "TON", cur: str = "RUB", tt: str = "SALE"):
        create = await self._post(
            "/p2p/public-api/v2/offer/create",
            {
                "type": tt,
                "initVolume": {"currencyCode": coin, "amount": f"{amount}"},
                "orderRoundingRequired": False,
                "price": {"type": "FLOATING", "baseCurrencyCode": coin, "quoteCurrencyCode": cur, "value": "120"},
                "orderAmountLimits": {"min": "500", "max": "2000"},
                "paymentConfirmTimeout": "PT15M",
                "comment": "",
                "paymentDetailsIds": fiats,
            },
        )
        return create

    # 11 - ad_upd
    async def ad_upd(self, typ: str, offer_id: int, fiats: list[int], amount: int):
        upd = await self._post(
            "/p2p/public-api/v2/offer/edit",
            {
                "offerId": offer_id,
                "paymentConfirmTimeout": "PT15M",
                "type": typ,
                "orderRoundingRequired": False,
                "price": {"type": "FLOATING", "value": "120"},
                "orderAmountLimits": {"min": "500", "max": "2000"},
                "comment": "",
                "volume": f"{amount}",
                "paymentDetailsIds": fiats,
            },
        )
        return upd

    # 12 - ad_del
    async def ad_del(self, typ: str, offer_id: int):
        ad_del = await self._post("/p2p/public-api/v2/offer/delete", {"type": typ, "offerId": offer_id})
        return ad_del

    # 13 - ad_on
    async def ad_on(self, typ: str, offer_id: int):
        active = await self._post("/p2p/public-api/v2/offer/activate", {"type": typ, "offerId": offer_id})
        return active

    # 14 - ad_off
    async def ad_off(self, typ: str, offer_id: int) -> dict[str, str]:
        off = await self._post("/p2p/public-api/v2/offer/deactivate", {"type": typ, "offerId": offer_id})
        return off

    # 15 - order_approve
    async def order_approve(self, order_id: int, typ: str):
        approve = await self._post("/p2p/public-api/v2/offer/order/accept", {"orderId": order_id, "type": typ})
        return approve

    # 16 - order_reject
    async def order_reject(self, order_id: str):
        reject = await self._post("/p2p/public-api/v2/offer/order/cancel/by-seller", {"orderId": order_id})
        return reject

    async def upload_file(self, order_id: int, path_to_file: str):
        url = f"public-api/v2/file-storage/file/upload?orderId={order_id}&uploadType=UPLOAD_BUYER_PAYMENT_RECEIPT"
        data = {"file": open(path_to_file, "rb")}
        upload_file = await self._post(url, data)
        return upload_file

    # 19 - order_paid
    async def order_paid(self, order_id: str, file: dict):
        paid = await self._post(
            "/p2p/public-api/v2/offer/order/confirm-sending-payment", {"orderId": order_id, "paymentReceipt": file}
        )
        return paid

    # 20 - order_payment_confirm
    async def order_payment_confirm(self, order_id: str):
        payment_confirm = await self._post("/p2p/public-api/v2/payment-details/confirm", {"orderId": order_id})
        return payment_confirm
