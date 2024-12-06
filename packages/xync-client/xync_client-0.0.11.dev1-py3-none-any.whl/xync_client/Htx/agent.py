from x_client.aiohttp import Client


class Public(Client):
    url_ads_web = "https://www.huobi.com/en-us/fiat-crypto/trade/"


class Private(Client):
    base_url = ""
    middle_url = ""

    htok: str = "Ev5lFfAvxDU2MA9BJ-Mc4U6zZG3Wb6qsp3Tx2fz6GIoY-uOP2m0-gvjE57ad1qDF"

    url_ads_req = "https://otc-cf.huobi.com/v1/data/trade-market"
    url_my_ads = "https://otc-api.trygofast.com/v1/data/trade-list?pageSize=50"
    url_my_ad = "https://www.huobi.com/-/x/otc/v1/otc/trade/"  # + id
    url_my_bals = "https://www.huobi.com/-/x/otc/v1/capital/balance"
    url_paccs = "https://www.huobi.com/-/x/otc/v1/user/receipt-account"
