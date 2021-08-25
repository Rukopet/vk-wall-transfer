import json
from pprint import pprint
from typing import Optional, List, Dict, Any

import requests
from telebot import TeleBot

from data.class_msg import Message
from data.config import TG_GROUP
from data.posgresql_class import PgDB

Url = str
PhotoFile = Any
Response = Dict


class MyTeleBot(TeleBot):
    def __init__(self, import_name, api_key):
        super().__init__(import_name)
        self.config = dict(
            api_key=api_key,
            requests_kwargs=dict(
                timeout=60,
            ),
        )

    def send_comment(self, reply_id: int,
                     text: str = '',
                     photo: List[Dict] = None) -> Response:

        if photo is not None:
            return self.send_photos(photo, text, reply_id)
        data = dict(
            chat_id=TG_GROUP,
            text=text,
            reply_to_message_id=reply_id
        )
        return self._bot_cmd(requests.post, 'sendMessage', data=data)

    def _send_media_group(self, data: dict,
                          photos: List[Dict],
                          caption: str,
                          reply_to_message_id: int = None) -> Response:

        data['media'] = json.dumps([
            {'type': 'photo',
             'caption': caption,
             'media': val.get('photo')}
            for val in photos
        ])
        if reply_to_message_id is not None:
            data['reply_to_message_id'] = reply_to_message_id
        return self._bot_cmd(requests.post, 'sendMediaGroup', data=data)

    def send_photos(self, photos: List[Dict],
                    caption: str = None,
                    reply_to_message_id: int = None) -> Response:

        data = dict(
            chat_id=TG_GROUP,
        )
        if photos is not None:
            if len(photos) > 1:
                return self._send_media_group(data, photos, caption, reply_to_message_id)
        if caption is not None:
            data['caption'] = caption
        if reply_to_message_id is not None:
            data['reply_to_message_id'] = reply_to_message_id
        data['photo'] = photos[0].get('photo')
        return self._bot_cmd(requests.post, 'sendPhoto', data=data)


class telegram_wall:
    @staticmethod
    def _send_message(bot: MyTeleBot, chat_id: int, mes: Message) -> Response:
        msg_text = f'{mes.fullname} написал на стене:\n{mes.text}'
        if mes.attachments is not None:
            return bot.send_photos(mes.attachments, msg_text)
        else:
            return bot.send_message(chat_id=chat_id, text=msg_text)

    @classmethod
    def send_message_return_tg_post_id(cls, tg_bot: MyTeleBot, mes: Message) -> Optional[int]:

        # if wall message
        if mes.mes_type == PgDB.wall_msg:
            tg_message = cls._send_message(tg_bot, TG_GROUP, mes)
            ret = tg_message.get('result')
            if ret is not None:
                if type(ret) == list:
                    ret, = ret
                ret = ret.get('message_id')
            return ret

        # if comment for wall message
        elif mes.mes_type == PgDB.wall_msg_comment:
            id_for_comment = PgDB.get_linked_tg_post_id_for_comments(mes)
            if id_for_comment is not None:
                msg_text = f'{mes.fullname} прокомментировал пост:\n{mes.text}'
                pprint(tg_bot.send_comment(id_for_comment, msg_text, mes.attachments))
