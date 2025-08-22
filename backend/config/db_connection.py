# Python & Third Party Imports
from threading import Lock

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from config.settings import app_settings

Base = declarative_base()

DATABASE_URL = f"postgresql://{app_settings.DB_USERNAME}:{app_settings.DB_PASSWORD}@{app_settings.DB_HOST}:{app_settings.DB_PORT}/{app_settings.DB_NAME}"


class DatabaseService:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Singleton implementation."""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DatabaseService, cls).__new__(cls)
        return cls._instance

    def __init__(self, database_url):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.database_url = database_url

            self.engine = create_engine(
                self.database_url,
                echo=False,
                pool_pre_ping=True,
            )

            self.session_factory = sessionmaker(bind=self.engine)
            self.Session = scoped_session(self.session_factory)

    def get_session(self):
        """Get a new session."""
        try:
            return self.Session()
        except SQLAlchemyError as e:
            print(f"Error while getting session: {e}")
            return None

    def close_connection(self):
        """Close the database connection."""
        self.Session.remove()
        self.engine.dispose()


db_service = DatabaseService(database_url=DATABASE_URL)
