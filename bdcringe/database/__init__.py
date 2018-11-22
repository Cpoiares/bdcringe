import psycopg2
from bdcringe import config


class Database:
    @staticmethod
    def connect():
        return psycopg2.connect(
            host=config.db.host,
            database=config.db.database,
            user=config.db.user,
            password=config.db.password
        )
