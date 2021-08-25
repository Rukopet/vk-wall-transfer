from marshmallow.utils import INCLUDE
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll
from data import config
from data.class_msg import MessageSchema
from pprint import pprint
from marshmallow import EXCLUDE

# from data.posgresql_class import WallMsgTable
from data.config import TG_BOT_TOKEN
from data.posgresql_class import PgDB
from tg_webhook import telegram_wall, MyTeleBot


def get_tg_bot() -> MyTeleBot:
    return MyTeleBot('TELE_BOT', TG_BOT_TOKEN)


def main():
    # autorization by token of group bot 
    vk_session = VkApi(token=config.VK_TOKEN)

    # call the longpool api
    longpoll = VkBotLongPoll(vk_session, config.VK_GROUP_ID)

    # class api
    vk = vk_session.get_api()

    # waiting for events
    tg_bot = get_tg_bot()

    for event in longpoll.listen():
        obj = event.raw.get('object')
        # obj = d.get('object')
        schema = MessageSchema(unknown=EXCLUDE)
        # context let us use API inside schema
        schema.context = {"api": vk}
        mes = schema.load(obj)
        mes.linked_tg_post = telegram_wall.send_message_return_tg_post_id(tg_bot, mes)
        PgDB.create_record_db_with_vk_event(mes)
        pprint(mes)


if __name__ == '__main__':
    main()
