"""
Service module for handling project queries, filtering, and database synchronization.
All operations are synchronous to match FastAPI's synchronous def endpoints.
"""

from typing import List, Dict, Any, Optional
import logging
from database import get_projects_collection, check_db_connection
from models import PROJECTS_DATA

logger = logging.getLogger("portfolio.services.projects")


def seed_projects_if_needed() -> int:
    """
    Seeds the MongoDB projects collection with initial verified project data if currently empty.
    Returns the number of seeded documents.
    """
    is_connected, _ = check_db_connection()
    if not is_connected:
        return 0

    try:
        col = get_projects_collection()
        if col is None:
            return 0

        count = col.count_documents({})
        if count == 0:
            # Insert verified project records
            docs = [dict(p) for p in PROJECTS_DATA]
            res = col.insert_many(docs)
            logger.info(f"Seeded {len(res.inserted_ids)} projects into MongoDB.")
            return len(res.inserted_ids)
        else:
            # Synchronize fields with models.PROJECTS_DATA
            for p in PROJECTS_DATA:
                col.update_one({"id": p["id"]}, {"$set": dict(p)}, upsert=True)
            return count
    except Exception as exc:
        logger.warning(f"Project seeding check encountered: {exc}")
        return 0


def get_all_projects(technology: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieves all projects with optional filtering by technology and search keyword.
    Uses MongoDB if connected; otherwise falls back gracefully to the verified in-memory dataset.
    """
    is_connected, _ = check_db_connection()
    projects: List[Dict[str, Any]] = []

    if is_connected:
        try:
            col = get_projects_collection()
            if col is not None:
                # Seed on first read if empty
                if col.count_documents({}) == 0:
                    seed_projects_if_needed()

                cursor = col.find({}, {"_id": 0}).sort("order", 1)
                projects = list(cursor)
        except Exception as exc:
            logger.error(f"Error querying projects collection: {exc}")
            projects = []

    # Fallback to source-of-truth if MongoDB query was empty or disconnected
    if not projects:
        projects = [dict(p) for p in PROJECTS_DATA]

    # Apply in-memory filtering (consistent across MongoDB and fallback)
    filtered = projects

    if technology:
        tech_clean = technology.strip().lower()
        filtered = [
            p for p in filtered
            if any(tech_clean in t.lower() for t in p.get("technologies", []))
        ]

    if search:
        s_clean = search.strip().lower()
        filtered = [
            p for p in filtered
            if (
                s_clean in p.get("title", "").lower()
                or s_clean in p.get("tagline", "").lower()
                or s_clean in p.get("problem", "").lower()
                or s_clean in p.get("solution", "").lower()
                or any(s_clean in t.lower() for t in p.get("technologies", []))
            )
        ]

    return filtered


def get_project_by_id_or_slug(identifier: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a single project by slug or ID.
    """
    ident = identifier.strip().lower()
    is_connected, _ = check_db_connection()

    if is_connected:
        try:
            col = get_projects_collection()
            if col is not None:
                doc = col.find_one({"$or": [{"slug": ident}, {"id": ident}]}, {"_id": 0})
                if doc:
                    return doc
        except Exception as exc:
            logger.warning(f"Error finding project in DB: {exc}")

    # Fallback search in verified dataset
    for p in PROJECTS_DATA:
        if p["slug"].lower() == ident or p["id"].lower() == ident:
            return dict(p)

    return None
