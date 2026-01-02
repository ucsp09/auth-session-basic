from core.adapters.db.base_db import BaseDB
from core.adapters.db.json_file_db import JsonFileDB
from core.adapters.session_store.base_session_store import BaseSessionStore
from core.adapters.session_store.json_file_session_store import JsonFileSessionStore
from core.logger import Logger
from config.constants import DB_TYPE, SESSION_STORE_TYPE
from fastapi import Depends
from dao.user_dao import UserDao
from dao.resource_dao import ResourceDao
from typing import Optional  # Import Optional for Python 3.6 compatibility

# ---- Module-level variables ----
_db: Optional[BaseDB] = None
_session_store: Optional[BaseSessionStore] = None
logger = Logger.get_logger(__name__)

# ---- Factories ----
def _create_db() -> BaseDB:
    """Factory function to create the appropriate DB instance based on configuration."""
    logger.debug("Creating database instance...")
    try:
        if DB_TYPE == "json_file":
            logger.info("Initializing JsonFileDB as the database backend.")
            return JsonFileDB()
        else:
            logger.error(f"Unsupported DB_TYPE: {DB_TYPE}")
            raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")
    except Exception as e:
        logger.exception(f"Failed to create database instance. Error: {e}")
        raise

def _create_session_store() -> BaseSessionStore:
    """Factory function to create the appropriate Session Store instance based on configuration."""
    logger.debug("Creating session store instance...")
    try:
        if SESSION_STORE_TYPE == "json_file":
            logger.info("Initializing JsonFileSessionStore as the session store backend.")
            return JsonFileSessionStore()
        else:
            logger.error(f"Unsupported SESSION_STORE_TYPE: {SESSION_STORE_TYPE}")
            raise ValueError(f"Unsupported SESSION_STORE_TYPE: {SESSION_STORE_TYPE}")
    except Exception as e:
        logger.exception(f"Failed to create session store instance. Error: {e}")
        raise

# ---- Accessor Functions ----
def get_db() -> BaseDB:
    """Get the initialized DB instance."""
    global _db
    if _db is None:
        logger.error("Database instance is not initialized.")
        raise RuntimeError("Database instance is not initialized.")
    logger.debug("Returning the initialized database instance.")
    return _db

def get_session_store() -> BaseSessionStore:
    """Get the initialized Session Store instance."""
    global _session_store
    if _session_store is None:
        logger.error("Session store instance is not initialized.")
        raise RuntimeError("Session store instance is not initialized.")
    logger.debug("Returning the initialized session store instance.")
    return _session_store

def get_user_dao(db: BaseDB = Depends(get_db)) -> UserDao:
    """Get an instance of UserDao with the provided DB dependency."""
    logger.debug("Creating UserDao instance.")
    return UserDao(db)

def get_resource_dao(db: BaseDB = Depends(get_db)) -> ResourceDao:
    """Get an instance of ResourceDao with the provided DB dependency."""
    logger.debug("Creating ResourceDao instance.")
    return ResourceDao(db)

# ---- Initialization and Cleanup ----
async def startup_event_handler():
    """Initialize the core components during the app startup."""
    global _db, _session_store
    logger.info("Starting up core components...")
    try:
        logger.debug("Creating database instance...")
        _db = _create_db()
        await _db.initialize()
        logger.info("Database initialized successfully.")

        logger.debug("Creating session store instance...")
        _session_store = _create_session_store()
        await _session_store.initialize()
        logger.info("Session store initialized successfully.")
    except Exception as e:
        logger.exception(f"Failed to initialize core components during startup. Error: {e}")
        raise

async def shutdown_event_handler():
    """Cleanup the core components during the app shutdown."""
    global _db, _session_store
    logger.info("Shutting down core components...")
    try:
        if _db is not None:
            logger.debug("Cleaning up database instance...")
            await _db.cleanup()
            logger.info("Database cleaned up successfully.")
            _db = None
        else:
            logger.warning("Database instance is already None during shutdown.")

        if _session_store is not None:
            logger.debug("Cleaning up session store instance...")
            await _session_store.cleanup()
            logger.info("Session store cleaned up successfully.")
            _session_store = None
        else:
            logger.warning("Session store instance is already None during shutdown.")
    except Exception as e:
        logger.exception(f"Failed to clean up core components during shutdown. Error: {e}")
        raise
        