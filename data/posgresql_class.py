from pprint import pprint
from typing import Any, Tuple, Type

from data.class_msg import Message
from data.config import DB_HOST, DB_PASS, DB_NAME, DB_USER
from psycopg2 import connect


class TableBase:
    FIELDS: Tuple[str] = None
    NAME_TABLE: str = None
    HAVE_JSON: bool = False

    @classmethod
    def fields_to_str(cls) -> str:
        """ returning format -> str1, str2, str3 """
        return ", ".join(cls.FIELDS)


class WallMsgTable(TableBase):
    """ Attachments(JSON field) always last field """

    FIELDS: Tuple[str] = ('post_id',
                          'user_id',
                          'fullname',
                          'text',
                          'date_create',
                          'linked_tg_post',
                          'attachments')
    NAME_TABLE: str = 'vk_wall_msg'
    HAVE_JSON: bool = True


class CommentsTable(TableBase):
    """ Attachments(JSON field) always last field """

    FIELDS: Tuple[str] = ('post_id',
                          'user_id',
                          'fullname',
                          'text',
                          'date_create',
                          'linked_id',
                          'attachments')
    NAME_TABLE: str = 'vk_wall_comments'
    HAVE_JSON: bool = True


class PgDB:
    wall_msg = 'wall_post_new'
    wall_msg_comment = 'wall_reply_new'

    @classmethod
    def _connection_with_db(cls):  # returning psycopg2 connect
        return connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

    @classmethod
    def message_to_table(cls, vk_message: Message, table: Type[TableBase]) -> None:
        with cls._connection_with_db() as conn:
            with conn.cursor() as cur:
                # req = sql.SQL('INSERT INTO {table} VALUES ({})')
                req = f'INSERT INTO {table.NAME_TABLE} ({table.fields_to_str()}) ' \
                      f'VALUES ({vk_message.to_str_for_db(table)})'
                cur.execute(req)
                conn.commit()

    @classmethod
    def create_record_db_with_vk_event(cls, vk_message: Message, vk_event: Any = None) -> None:
        if vk_message.mes_type == cls.wall_msg:
            cls.message_to_table(vk_message, WallMsgTable)
        elif vk_message.mes_type == cls.wall_msg_comment:
            cls.message_to_table(vk_message, CommentsTable)

    @classmethod
    def get_linked_tg_post_id_for_comments(cls, vk_message: Message) -> int:
        with cls._connection_with_db() as conn:
            with conn.cursor() as cur:
                req = f'SELECT linked_tg_post FROM {WallMsgTable.NAME_TABLE}' \
                      f' WHERE post_id = {vk_message.linked_id}'
                cur.execute(req)
                ret = cur.fetchone()
        return ret[0]
