import psycopg2
from psycopg2 import pool

class DatabaseConnector:
    _instance = None  # Atributo de clase para almacenar la única instancia

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self, dsn):
        if not hasattr(self, '_initialized'):
            self._initialized = True  # Asegura que __init__ se ejecute solo una vez
            self._connection_pool = None
            self.dsn = dsn

    def initialize_connection_pool(self, minconn=1, maxconn=10):
        if not self._connection_pool:
            self._connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn, maxconn, self.dsn
            )

    def get_connection(self):
        if not self._connection_pool:
            raise Exception("Connection pool is not initialized. Call 'initialize_connection_pool' first.")
        return self._connection_pool.getconn()

    def release_connection(self, connection):
        if self._connection_pool:
            self._connection_pool.putconn(connection)

    def close_all_connections(self):
        if self._connection_pool:
            self._connection_pool.closeall()