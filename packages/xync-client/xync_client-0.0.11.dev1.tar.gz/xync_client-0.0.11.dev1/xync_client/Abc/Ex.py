import logging
import re
from abc import abstractmethod

from xync_client.Abc.Base import BaseClient, DictOfDicts, FlatDict, ListOfDicts, MapOfIdsList
from xync_schema.models import Ex, Coin, Cur, Pm, Pmex, Curex, Pmcur, Pmcurex, Coinex


class BaseExClient(BaseClient):
    ex: Ex
    pm_map: dict[str, str] = {
        "Юmoney": "YooMoney",
        "Local Bank (R-Green)": "Sberbank",
        "Local Bank (S-Green)": "Sberbank",
        "Local Card (Red)": "Alfa-Bank",
        "Local Card (Yellow)": "Tinkoff",
        "Local Card M-redTS": "MTS-bank",
        "Local Card-Green": "Sberbank",
        "Local Card-Yellow": "Tinkoff",
        "GTB Bank (Guarantee Trust Bank)": "GTBank",
    }

    def __init__(self, ex: Ex):
        self.ex = ex
        self.acronyms: dict[str, str] = {}  # for pm norm
        super().__init__(ex)

    # 20: Список всех платежных методов на бирже
    @abstractmethod
    async def pms(self) -> DictOfDicts:  # {pm.exid: pm}
        ...

    # 21: Список поддерживаемых валют
    @abstractmethod
    async def curs(self) -> FlatDict:  # {cur.exid: cur.ticker}
        ...

    # 22: Список платежных методов по каждой валюте
    @abstractmethod
    async def cur_pms_map(self) -> MapOfIdsList:  # {cur.exid: [pm.exid]}
        ...

    # 23: Список торгуемых монет (с ограничениям по валютам, если есть)
    @abstractmethod
    async def coins(self) -> FlatDict:  # {coin.exid: coin.ticker}
        ...

    # 24: Список объяв по (buy/sell, cur, coin, pm)
    @abstractmethod
    async def ads(
        self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None
    ) -> ListOfDicts:  # {ad.id: ad}
        ...

    def _pmnorm(self, s: str) -> str:
        def get_and_remove_acro(title: str) -> str:
            acr = "".join(word[0] for word in title.split(" ") if len(word) > 1 and word.istitle())
            if len(acr) > 2:
                title = title.replace(acr, "", 1)
                self.acronyms[acr] = title  # заполняем словарь аббревиатур
            return title

        def find_and_replace_only_acro(title: str) -> str:
            if " " not in title and title.isupper() and title in self.acronyms:
                title = self.acronyms[title]
            return title

        def remove(rms: str | list[str], st: str, regexp: bool = False) -> str:
            for rm in rms:
                st = re.sub(rm, "", st) if regexp else st.replace(rm, "")
            return st

        s = get_and_remove_acro(s)
        s = find_and_replace_only_acro(s)
        s = self.pm_map.get(s, s)
        s = s.lower().strip()
        s = remove("-:`'’′", s)
        common_map = {
            "nationale": "national",
            "а": "a",
            "á": "a",
            "â": "a",
            "о": "o",
            "ó": "o",
            "ō": "o",
            "ú": "u",
            "ü": "u",
            "ų": "u",
            "с": "c",
            "č": "c",
            "ç": "c",
            "é": "e",
            "è": "e",
            "ş": "s",
            "š": "s",
            "ř": "r",
            "í": "i",
        }
        for src, trgt in common_map.items():
            s = s.replace(src, trgt)
        rm_rgxps = [
            r"\(card\)$|\(russia\)$",
            r"^bank\s|bank$",
            r"^banka\s|\sbanka$",
            r"^bankas\s|\sbankas$",
            r"^bankası\s|\sbankası$",
            r"^banca\s|\sbanca$",
            r"^banco\s|\sbanco$",
            r"\.io$|\.com$",
            r"s\.a$",
        ]
        s = remove(rm_rgxps, s, True)
        return s.replace(" ", "")

    async def set_pmcurexs(self):
        # Pms
        pmsd = {k: v for k, v in sorted((await self.pms()).items(), key=lambda x: x[1]["name"])}  # sort by name
        pms: dict[int | str, Pm] = dict({})
        prev = 0, "", ""  # id, normd-name, orig-name
        for k, pm in pmsd.items():
            norm = self._pmnorm(pm["name"])
            if prev[1:] == (norm, pm["name"]):
                logging.warning(f"Pm: '{pm['name']}' duplicated with ids {prev[0]}: {k} on {self.ex.name}")
                pm_ = pms.get(prev[0], (await Pm.get_or_none(name=prev[2])) or await Pm.get_or_none(identifier=prev[1]))
                await Pmex.update_or_create({"pm": pm_}, ex=self.ex, exid=k, name=pm["name"])
            elif prev[1] == norm:
                logging.error(
                    f"Pm: '{pm['name']}' & '{prev[2]}' overnormd as '{norm}' with ids {prev[0]}: {k} on {self.ex.name}"
                )
                await Pmex.update_or_create(
                    {"pm": pms.get(prev[0], await Pm.get(name=prev[2]))}, ex=self.ex, exid=k, name=pm["name"]
                )
            else:
                pms[k], _ = await Pm.update_or_create(pm, identifier=norm)
            prev = k, norm, pm["name"]
        # Pmexs
        pmexs = [Pmex(exid=k, ex=self.ex, pm=pm, name=pm.name) for k, pm in pms.items()]
        await Pmex.bulk_create(pmexs, ignore_conflicts=True)
        # Curs
        cursd = await self.curs()
        curs: {int: Cur} = {k: (await Cur.update_or_create(ticker=c))[0] for k, c in cursd.items()}
        # Curex
        curexs = [Curex(cur=c, ex=self.ex, exid=k) for k, c in curs.items()]  # , p2p=True
        await Curex.bulk_create(curexs, ignore_conflicts=True)

        cur2pms = await self.cur_pms_map()
        # # Link PayMethods with currencies
        pmcurs = set()
        [
            [
                pmcurs.add(
                    (
                        await Pmcur.update_or_create(
                            cur=curs[cur_id],
                            pm=pms.get(exid, (await Pmex.get(ex=self.ex, exid=prev[0]).prefetch_related("pm")).pm),
                        )
                    )[0]
                )
                for exid in exids
            ]
            for cur_id, exids in cur2pms.items()
        ]
        pmcurexs = [Pmcurex(pmcur=pmcur, ex=self.ex) for pmcur in pmcurs]
        await Pmcurex.bulk_create(pmcurexs)

    async def set_coinexs(self):
        res = await self.coins()
        coins: dict[int, Coin] = {k: (await Coin.update_or_create(ticker=c))[0] for k, c in res.items()}
        coinexs: list[Coinex] = [Coinex(coin=c, ex=self.ex, exid=k) for k, c in coins.items()]
        await Coinex.bulk_create(coinexs, ignore_conflicts=True)
