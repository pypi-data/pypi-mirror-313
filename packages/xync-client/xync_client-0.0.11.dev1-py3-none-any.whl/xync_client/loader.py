from dotenv import load_dotenv
from os import getenv as env

load_dotenv()
PG_DSN = f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST', 'xyncdbs')}:{env('POSTGRES_PORT', 5432)}/{env('POSTGRES_DB', env('POSTGRES_USER'))}"

HT = env("HT")
BKEY = env("BKEY")
BSEC = env("BSEC")
OKXKEY = env("OKXKEY")
OKXSEC = env("OKXSEC")
OKXPSF = env("OKXPSF")
BYT = env("BYT")
BYTP2P = env("BYTP2P")
BYT2FA = env("BYT2FA")
BYKEY = env("BYKEY")
BYSEC = env("BYSEC")
GATE_UID = env("GATE_UID")
GATE_PVER = env("GATE_PVER")
KUKEY = env("KUKEY")
KUSEC = env("KUSEC")
CMXK = env("CMXK")
CMXS = env("CMXS")
