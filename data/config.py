from environs import Env

env = Env()
env.read_env()

VK_TOKEN = env.str("VK_TOKEN")
VK_GROUP_ID = env.int("VK_GROUP_ID")
TG_URL = env.str("TELEGRAM_URL")
TG_BOT_TOKEN = env.str("TG_BOT_TOKEN")
TG_GROUP = env.str('TG_GROUP')
TG_GROUP_COMMENT = env.str('TG_GROUP_COMMENT')

DB_HOST = env.str("DB_HOST")
DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
