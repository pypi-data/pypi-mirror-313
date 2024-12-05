import os
import threading

from psycopg_pool import AsyncConnectionPool

class PostgresAsyncConnectionPool:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(PostgresAsyncConnectionPool, cls).__new__(cls)
                    cls._instance._initialize_pool()
        return cls._instance
    
    def _initialize_pool(self):
        db_host = os.getenv("CHECKPOINT_DB_HOST")
        db_name = os.getenv("DB_NAME", "postgres")
        db_user = os.getenv("CHECKPOINT_DB_USER","postgres")
        db_password = os.getenv("CHECKPOINT_DB_PASSWORD")
        db_port = os.getenv("CHECKPOINT_DB_PORT", "5432")
        db_max_connections = int(os.getenv("DB_MAX_CONNECTIONS", "10"))

        db_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=disable"

        connection_pool = AsyncConnectionPool(conninfo=db_uri,
            max_size=db_max_connections,
            kwargs={
                "autocommit": True,
                "prepare_threshold": 0,
            },
        )

        self.pool = connection_pool

    def get(self):
        return self.pool