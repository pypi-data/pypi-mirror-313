from urllib.parse import parse_qs
from pyrogram import Client
from pyrogram.raw import functions
from xync_schema.models import Agent


class PyroClient:
    api_id = 20276309
    api_hash = "077f4a2aa1debc0768c582c818d20f64"

    def __init__(self, agent: Agent):
        self.app: Client = Client(str(agent.user_id), self.api_id, self.api_hash, session_string=agent.auth["sess"])

    async def get_init_data(self) -> dict:
        async with self.app as app:
            app: Client
            await app.send_message("me", "Greetings from **Pyrogram**!")
            bot = await app.resolve_peer("wallet")
            me = await app.resolve_peer(self.app.name)
            res = await app.invoke(functions.messages.RequestWebView(peer=me, bot=bot, platform="chatparse"))
            raw = parse_qs(res.url)["tgWebAppUserId"][0].split("#tgWebAppData=")[1]
            j = parse_qs(raw)
            return {
                "web_view_init_data": {
                    "query_id": j["query_id"][0],
                    "user": j["user"][0],
                    "auth_date": j["auth_date"][0],
                    "hash": j["hash"][0],
                },
                "web_view_init_data_raw": raw,
                "ep": "menu",
            }
