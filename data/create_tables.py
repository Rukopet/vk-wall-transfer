from typing import Any

import psycopg2
Cursor: Any


def create_tables(index: bool = True):
    from data.config import DB_HOST, DB_PASS, DB_NAME, DB_USER

    # port default 5432
    with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) as connection:
        with connection.cursor() as cursor:
            req = f"CREATE TABLE vk_wall_msg" \
                  f"(post_id INT8 NOT NULL PRIMARY KEY," \
                  f"user_id INT8," \
                  f"fullname VARCHAR," \
                  f"text VARCHAR," \
                  f"date_create DATE," \
                  f"linked_tg_post INT8," \
                  f"attachments JSON)"
            cursor.execute(req)
            req = f"CREATE TABLE vk_wall_comments" \
                  f"(post_id INT8 NOT NULL PRIMARY KEY," \
                  f"user_id INT8," \
                  f"fullname VARCHAR," \
                  f"text VARCHAR," \
                  f"date_create DATE," \
                  f"linked_id INT8," \
                  f"attachments JSON)"
            # f"linked_id INT8 REFERENCES vk_wall_msg(post_id)," \
            cursor.execute(req)
            connection.commit()
            req = f"CREATE INDEX post_id_wall ON vk_wall_msg(post_id, user_id)"
            cursor.execute(req)
            req = f"CREATE INDEX post_id_comment ON vk_wall_comments(post_id, user_id)"
            cursor.execute(req)
            connection.commit()


if __name__ == "__main__":
    create_tables()
