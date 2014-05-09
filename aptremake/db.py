import os


SQLITE3 = "sqlite3"
PSYCOPG2 = "psycopg2"


class Database(object):

    def __init__(self, driver, **kwargs):
        self.driver = driver
        self.driver_module = __import__(driver, globals(), locals(), [], -1)
        self.path = kwargs["path"]
        self.connection = None
        self.database = kwargs["database"]
        self.user = kwargs["user"]
        self.password = kwargs["password"]
        self.host = kwargs["host"]
        self.port = kwargs["port"]
        if not self.is_sqlite() and not self.is_postgres():
            raise ValueError("Unsupported Database Driver: " + str(self.driver))

    @property
    def wildcard(self):
        """
        Engine-specific character sequence to indicate query parameters
        in SQL statments.
        """

        if self.is_sqlite():
            return '?'
        elif self.is_postgres():
            return '%s'

    @property
    def exception_error_class(self):
        return self.driver_module.Error

    def escape_symbol(self, symbol):
        if symbol.literal:
            return self.wildcard

        if self.is_sqlite():
            return symbol.value
        elif self.is_postgres():
            return symbol.value.replace('%s', '%%s')

    def exception_info(self, exception):
        if self.is_sqlite():
            return exception.args[0]
        elif self.is_postgres():
            return ': '.join((exception.pgcode, exception.pgerror))

    def is_sqlite(self):
        return self.driver == SQLITE3 

    def is_postgres(self):
        return self.driver == PSYCOPG2

    def connect(self):
        if self.connection:
            return self # so that we can proxy calls to the connection.

        if self.is_sqlite():
            self.connection = self.driver_module.connect(self.path)

        elif self.is_postgres():
            self.connection = self.driver_module.connect(self.database, self.user,
                self.password, self.port, self.host)

        return self

    def execute(self, query, params=()):
        if not self.connection:
            raise ValueError("Must connect to database before running queries.")

        if self.is_sqlite():
            return self.connection.execute(query, params)

        elif self.is_postgres():
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor

    def close(self):
        self.connection.close()
        self.connection = None
