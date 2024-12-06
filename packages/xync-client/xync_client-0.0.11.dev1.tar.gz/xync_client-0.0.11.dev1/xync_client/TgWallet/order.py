from enum import StrEnum, IntEnum
from xync_schema.models import Order, OrderStatus

from xync_client.Abc.Order import BaseOrderClient


class Exceptions(StrEnum):
    PM_KYC = "OFFER_FIAT_COUNTRY_NOT_SUPPORTED_BY_USER_KYC_COUNTRY"


class Status(IntEnum):
    ALL_ACTIVE = OrderStatus.active


class OrderClient(BaseOrderClient):
    # 2
    async def cancel_request(self) -> Order:
        pass

    # 2
    async def accept_request(self) -> bool:
        approve = await self._post(
            "/p2p/public-api/v2/offer/order/accept",
            {"orderId": self.order.id, "type": {True: "SALE", False: "BUY"}[self.im_seller]},
        )
        return approve

    # 2
    async def reject_request(self) -> bool:
        reject = await self._post("/p2p/public-api/v2/offer/order/cancel/by-seller", {"orderId": self.order.id})
        return reject

    # 2
    async def mark_payed(self, receipt):
        pass

    # 2
    async def cancel_order(self) -> bool:
        pass

    # 7 - [S] payment received confirm
    async def confirm(self) -> bool:
        payment_confirm = await self._post("/p2p/public-api/v2/payment-details/confirm", {"orderId": self.order.id})
        return payment_confirm

    # 2
    async def start_appeal(self, file) -> bool:
        pass

    # 2
    async def dispute_appeal(self, file) -> bool:
        pass

    async def cancel_appeal(self) -> bool:
        pass

    # 2
    async def send_order_msg(self, msg: str, file=None) -> bool:
        pass

    # 2
    async def send_appeal_msg(self, file, msg: str = None) -> bool:
        pass

    # 2
    async def _upload_file(self, order_id: int, path_to_file: str):
        url = f"/public-api/v2/file-storage/file/upload?orderId={order_id}&uploadType=UPLOAD_BUYER_PAYMENT_RECEIPT"
        data = {"file": open(path_to_file, "rb")}
        upload_file = await self._post(url, data)
        return upload_file

    # 19 - order_paid
    async def order_paid(self, order_id: str, file: dict):
        paid = await self._post(
            "/p2p/public-api/v2/offer/order/confirm-sending-payment", {"orderId": order_id, "paymentReceipt": file}
        )
        return paid
