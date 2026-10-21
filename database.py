"""
MongoDB Atlas database connection module for Ashwini Samaneti's Portfolio.
Uses synchronous PyMongo operations designed for synchronous FastAPI endpoint execution.
Includes dynamic environment reloading, TLS/SSL root certificate verification via certifi,
and descriptive diagnostics for common Atlas Network Access / IP whitelist errors.
"""

import os
import logging
from typing import Optional, Tuple
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

try:
    import certifi
    _CA_FILE = certifi.where()
except Exception:
    _CA_FILE = None

logger = logging.getLogger("portfolio.database")

_client: Optional[MongoClient] = None
_last_uri: Optional[str] = None


def get_current_uri() -> str:
    """Dynamically retrieves MONGODB_URI from environment with live .env recheck."""
    load_dotenv(override=True)
    return os.getenv("MONGODB_URI", "").strip().strip('"').strip("'")


def get_current_database_name() -> str:
    return os.getenv("MONGODB_DATABASE", "ashwini_portfolio").strip()


def get_mongo_client() -> Optional[MongoClient]:
    """
    Returns a PyMongo client instance configured with
    timeouts and certifi CA certificates. Reconnects if MONGODB_URI changed.
    """
    global _client, _last_uri

    uri = get_current_uri()
    if not uri:
        _client = None
        _last_uri = None
        return None

    # If URI changed or client not yet created, instantiate new client
    if _client is None or uri != _last_uri:
        try:
            client_options = {
                "serverSelectionTimeoutMS": 3000,
                "connectTimeoutMS": 3000,
                "socketTimeoutMS": 3000,
                "retryWrites": True,
                "appname": "AshwiniPortfolioFastAPI"
            }
            if _CA_FILE:
                client_options["tlsCAFile"] = _CA_FILE

            _client = MongoClient(uri, **client_options)
            _last_uri = uri
        except Exception as exc:
            logger.error(f"Failed to initialize PyMongo client: {exc}")
            _client = None
            return None

    return _client


def get_database() -> Optional[Database]:
    """Returns the ashwini_portfolio Database instance, or None if unavailable."""
    client = get_mongo_client()
    if client is None:
        return None
    return client[get_current_database_name()]


def get_collection(collection_name: str) -> Optional[Collection]:
    """Returns a specific collection from the database, or None if disconnected."""
    db = get_database()
    if db is None:
        return None
    return db[collection_name]


def get_contacts_collection() -> Optional[Collection]:
    return get_collection("contacts")


def get_projects_collection() -> Optional[Collection]:
    return get_collection("projects")


def check_db_connection() -> Tuple[bool, str]:
    """
    Checks live database connectivity without leaking credentials.
    Provides clear diagnostics for IP Whitelist / Network Access alerts.
    Returns (is_connected: bool, message: str).
    """
    uri = get_current_uri()
    if not uri:
        return False, "MONGODB_URI is not configured in .env. Live database connectivity remains unverified."

    client = get_mongo_client()
    if client is None:
        return False, "Failed to instantiate PyMongo client with current configuration."

    try:
        # Run a lightweight ping command with strict timeout
        client.admin.command("ping")
        return True, "Successfully connected to MongoDB Atlas cluster."
    except (ConnectionFailure, ServerSelectionTimeoutError) as err:
        err_str = str(err)
        if "TLSV1_ALERT_INTERNAL_ERROR" in err_str or "SSL handshake failed" in err_str:
            return (
                False,
                "MongoDB Atlas rejected connection (TLSV1_ALERT_INTERNAL_ERROR). "
                "Your IP address is not whitelisted in MongoDB Atlas Network Access. "
                "Please add 0.0.0.0/0 (or your current IP) under Atlas -> Network Access."
            )
        return False, f"Could not reach MongoDB Atlas cluster: {type(err).__name__}. Check network and credentials."
    except Exception as exc:
        return False, f"Database connectivity error: {type(exc).__name__}"


def init_indexes() -> None:
    """
    Ensures optimal indexes exist on collections if the database is accessible.
    """
    is_connected, _ = check_db_connection()
    if not is_connected:
        return

    try:
        projects_col = get_projects_collection()
        if projects_col is not None:
            projects_col.create_index([("slug", ASCENDING)], unique=True)
            projects_col.create_index([("order", ASCENDING)])
            logger.info("Project collection indexes verified.")

        contacts_col = get_contacts_collection()
        if contacts_col is not None:
            contacts_col.create_index([("created_at", DESCENDING)])
            contacts_col.create_index([("email", ASCENDING)])
            logger.info("Contact collection indexes verified.")
    except Exception as exc:
        logger.warning(f"Note on index creation: {exc}")
