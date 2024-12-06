from typing import TypeGuard

from xync_client.Abc.Base import DictOfDicts, ListOfDicts, FlatDict, MapOfIdsList


class BaseTest:
    @staticmethod
    def is_dod(dct: DictOfDicts) -> TypeGuard[DictOfDicts]:
        return all(isinstance(k, int | str) and isinstance(v, dict) for k, v in dct.items())

    @staticmethod
    def is_lod(lst: ListOfDicts) -> TypeGuard[ListOfDicts]:
        return all(isinstance(el, dict) for el in lst)

    @staticmethod
    def is_fd(dct: FlatDict) -> TypeGuard[FlatDict]:
        return all(isinstance(k, int | str) and isinstance(v, str) for k, v in dct.items())

    @staticmethod
    def is_moil(dct: MapOfIdsList) -> TypeGuard[MapOfIdsList]:
        return all(isinstance(k, int | str) and isinstance(v, str) for k, v in dct.items())
