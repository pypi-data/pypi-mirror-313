from abc import abstractmethod

from xync_client.Abc.Auth import BaseAuthClient
from xync_schema.enums import PmType
from xync_schema.models import OrderStatus, Coin, Cur, Order, Pm, Ad, AdStatus, Fiat
from xync_schema.pydantic import FiatNew


class BaseAgentClient(BaseAuthClient):
    # 0: Получшение ордеров в статусе status, по монете coin, в валюте coin, в направлении is_sell: bool
    @abstractmethod
    async def get_orders(
        self, stauts: OrderStatus = OrderStatus.active, coin: Coin = None, cur: Cur = None, is_sell: bool = None
    ) -> list[Order]: ...

    # 1: [T] Получшение ордеров в статусе status, по монете coin, в валюте coin, в направлении is_sell: bool
    @abstractmethod
    async def order_request(self, ad_id: int, amount: float) -> dict: ...

    # async def start_order(self, order: Order) -> OrderOutClient:
    #     return OrderOutClient(self, order)

    # # # Fiat
    # 25: Список реквизитов моих платежных методов
    @abstractmethod
    async def my_fiats(self, cur: Cur = None) -> list[dict]: ...

    # 26: Создание
    @abstractmethod
    async def fiat_new(self, fiat: FiatNew) -> Fiat.pyd(): ...

    # 27: Редактирование
    @abstractmethod
    async def fiat_upd(self, detail: str = None, type_: PmType = None) -> bool: ...

    # 28: Удаление
    @abstractmethod
    async def fiat_del(self, fiat_id: int) -> bool: ...

    # # # Ad
    # 29: Список моих ad
    @abstractmethod
    async def my_ads(self) -> list[dict]: ...

    # 30: Создание ad:
    @abstractmethod
    async def ad_new(
        self,
        coin: Coin,
        cur: Cur,
        is_sell: bool,
        pms: list[Pm],
        price: float,
        is_float: bool = True,
        min_fiat: int = None,
        details: str = None,
        autoreply: str = None,
        status: AdStatus = AdStatus.active,
    ) -> Ad: ...

    # 31: Редактирование
    @abstractmethod
    async def ad_upd(
        self,
        pms: [Pm] = None,
        price: float = None,
        is_float: bool = None,
        min_fiat: int = None,
        details: str = None,
        autoreply: str = None,
        status: AdStatus = None,
    ) -> bool: ...

    # 32: Удаление
    @abstractmethod
    async def ad_del(self) -> bool: ...

    # 33: Вкл/выкл объявления
    @abstractmethod
    async def ad_switch(self) -> bool: ...

    # 34: Вкл/выкл всех объявлений
    @abstractmethod
    async def ads_switch(self) -> bool: ...

    # # # User
    # 35: Получить объект юзера по его ид
    @abstractmethod
    async def get_user(self, user_id) -> dict: ...

    # 36: Отправка сообщения юзеру с приложенным файло
    @abstractmethod
    async def send_user_msg(self, msg: str, file=None) -> bool: ...

    # 37: (Раз)Блокировать юзера
    @abstractmethod
    async def block_user(self, is_blocked: bool = True) -> bool: ...

    # 38: Поставить отзыв юзеру
    @abstractmethod
    async def rate_user(self, positive: bool) -> bool: ...
