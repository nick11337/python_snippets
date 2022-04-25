import psycopg2
import psycopg2.extras
from psycopg2 import errors

import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DatabaseHandler(object):
    def __init__(self, host, db_name, username, password):
        self.DB_CONNECTION = {
            "db_host": host,
            "db_name": db_name,
            "db_username": username,
            "db_password": password,
        }

        self.connection = self.get_conn()

    def get_conn(self):
        return DatabaseHandler.create_conn(
            DatabaseHandler.get_conn_string(self.DB_CONNECTION)
        )

    @staticmethod
    def get_conn_string(db_conn):
        return "dbname='{}' port='5432' user='{}' password='{}' host='{}'".format(
            db_conn["db_name"],
            db_conn["db_username"],
            db_conn["db_password"],
            db_conn["db_host"],
        )

    @staticmethod
    def create_conn(conn_string):
        try:
            connection = psycopg2.connect(conn_string)
        except psycopg2.OperationalError:
            raise psycopg2.OperationalError
        return connection

    @staticmethod
    def execute_update(con, cur, script):
        UniqueViolation = errors.lookup("23505")

        try:
            cur.execute(script)
            con.commit()
            result = True
        except UniqueViolation as e:
            con.rollback()
            raise UniqueViolation
        except Exception as e:
            con.rollback()
            raise e
            # con.close() #Todo Close Connection?

        return result

    @staticmethod
    def execute_query(con, cur, script):
        InvalidTextViolation = errors.lookup("22P02")

        try:
            cur.execute(script)
            con.commit()
            result = cur.fetchall()
        except InvalidTextViolation as e:
            con.rollback()
            raise e

        except Exception as e:
            con.rollback()
            raise e

        return result

    def run_update(self, script):
        con = self.connection
        return DatabaseHandler.execute_update(con, con.cursor(), script)

    def run_query(self, script):
        con = self.connection
        return DatabaseHandler.execute_query(
            con, con.cursor(cursor_factory=psycopg2.extras.RealDictCursor), script
        )





