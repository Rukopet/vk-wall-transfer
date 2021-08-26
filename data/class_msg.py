from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from marshmallow import Schema, fields, post_load
from marshmallow.utils import EXCLUDE
from vk_api import exceptions

Table = Any


@dataclass
class Attachment:
    photo: Dict


class AttachmentSchema(Schema):
    photo = fields.Dict()


def wrap_str_into_quotes(string: str) -> str:
    return "\'" + string + "\'"


@dataclass
class Message:
    post_id: int
    user_id: int
    date_create: int
    text: str = ""
    attachments: Optional[List[Dict]] = None
    mes_type: str = ""
    linked_id: int = 0
    fullname: str = ""
    linked_tg_post: Optional[int] = None

    def to_str_for_db(self, table: Table) -> str:
        """ returning format -> str1, str2, str3 """
        tmp_list = []
        from datetime import datetime
        for db_column in table.FIELDS:
            string = self.__dict__[db_column]
            if type(string) == str:
                tmp_list.append(wrap_str_into_quotes(string))
            elif type(string) == dict or type(string) == list:
                import json
                string = json.dumps(string)
                tmp_list.append(wrap_str_into_quotes(str(string)))
            elif string is None:
                tmp_list.append("null")
            elif db_column == "date_create":
                string = datetime.fromtimestamp(string)
                tmp_list.append(wrap_str_into_quotes(str(string)))
            else:
                tmp_list.append(str(string))
        return ", ".join(tmp_list)


class MessageSchema(Schema):
    post_id = fields.Integer(data_key="id")
    user_id = fields.Integer(data_key='from_id')
    fullname = fields.String(missing='Unknown', default='Unknown')
    text = fields.String()
    date_create = fields.Integer(data_key='date')
    attachments = fields.Nested(AttachmentSchema, many=True, required=False, unknown=EXCLUDE)
    mes_type = fields.String(data_key='type')
    linked_id = fields.Integer(data_key='post_id')

    def _get_name(self, user_id: int) -> str:
        vk = self.context['api']
        try:
            response = vk.users.get(user_ids=user_id)
            fullname = response[0].get('first_name') + ' ' + response[0].get('last_name')
        except exceptions.ApiError:
            response = vk.groups.getById(group_ids=user_id)
            fullname = response[0].get('name')
        except Exception:
            fullname = 'cant get it from API'
        return fullname

    @staticmethod
    def _get_url(photo: Dict) -> str:
        sizes = photo.get('sizes')
        if sizes is None:
            return ""
        photo_sizes = {
            size.get('height'): size.get('url')
            for size in sizes
        }
        max_url_photo = photo_sizes[max(photo_sizes.keys())]
        return max_url_photo

    @post_load
    def make_message(self, data, **kwargs):
        data['fullname'] = self._get_name(data.get('user_id'))
        data['mes_type'] = "wall_post_new" if data.get('linked_id') is None else "wall_reply_new"
        tmp = data.get('attachments')
        if tmp is None:
            return Message(**data)
        data['attachments'] = [
            {'photo': self._get_url(att.get('photo'))}
            for att in tmp
            if att.get('photo') is not None
        ]
        return Message(**data)
