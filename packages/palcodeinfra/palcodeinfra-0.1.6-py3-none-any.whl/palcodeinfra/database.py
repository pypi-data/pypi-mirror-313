from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import pkgutil
import importlib

Base = declarative_base()

class Database:
    def __init__(self, database_url: str):
        self._engine = create_engine(database_url)
        self._SessionLocal = sessionmaker(bind=self._engine, autocommit=False, autoflush=False)
        # if dataaccess_model_path:
        #     modelpath = f"{dataaccess_model_path}.__path__"
        #     for _, module_name, _ in pkgutil.iter_modules(modelpath):
        #         importlib.import_module(f"{dataaccess_model_path}.{module_name}")
        
        # Create all tables in the database
        Base.metadata.create_all(self._engine)

    def get_engine(self) -> Engine:
        return self._engine

    def get_session_local(self) -> sessionmaker:
        return self._SessionLocal

    def create_session(self) -> Session:
        """Creates and returns a new session"""
        return self._SessionLocal()

    def close_session(self, session: Session):
        """Closes the given session"""
        session.close()

    def create_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self._engine)