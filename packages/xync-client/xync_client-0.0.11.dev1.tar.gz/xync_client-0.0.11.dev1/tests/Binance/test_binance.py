from x_model import init_db
from xync_client.loader import PG_DSN
from xync_schema import models
from xync_schema.models import Ex


async def test_cur_filter():
    _ = await init_db(PG_DSN, models, True)
    ex = await Ex.get(name="Binance")
    bn = await ex.client()
    resp = await bn.cur_pms_map()
    assert len(resp[0]) and len(resp[1]), "No data"
