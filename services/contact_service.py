"""
Service module for validating and saving contact form submissions to MongoDB.
Follows strict security practices: no credential leakage, spam protection, and real status reporting.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
import logging
from fastapi import HTTPException, status
from database import get_contacts_collection, check_db_connection
from schemas import ContactCreate

logger = logging.getLogger("portfolio.services.contacts")


def handle_contact_submission(data: ContactCreate, client_ip: str = "unknown") -> Dict[str, Any]:
    """
    Validates anti-spam honeypot and persists contact submission to MongoDB.
    Raises HTTPException(503) if database is unavailable — never fakes success.
    """
    # 1. Anti-spam honeypot check: If hidden field 'website' is filled, silently reject or fail
    if data.website:
        logger.warning(f"Spam honeypot triggered from IP: {client_ip}")
        # Return a generic failure to not tip off automated scrapers
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spam validation failed. Please submit the form normally."
        )

    # 2. Check live MongoDB connectivity
    is_connected, db_message = check_db_connection()
    if not is_connected:
        logger.error(f"Contact submission attempted but MongoDB is disconnected: {db_message}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Database connectivity is currently unverified. Submission was not recorded. "
                "Please configure MONGODB_URI in your environment or email Ashwini directly at ashwinisamaneti@gmail.com."
            )
        )

    col = get_contacts_collection()
    if col is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database collection handle unavailable. Please reach out via email: ashwinisamaneti@gmail.com."
        )

    # 3. Build document with ISO timestamp and client metadata
    now_utc = datetime.now(timezone.utc)
    document = {
        "name": data.name,
        "email": data.email,
        "subject": data.subject or "Portfolio Inquiry",
        "message": data.message,
        "client_ip": client_ip,
        "created_at": now_utc,
        "status": "unread"
    }

    try:
        result = col.insert_one(document)
        logger.info(f"Successfully recorded contact submission {result.inserted_id} from {data.email}")
        return {
            "success": True,
            "message": "Thank you! Your message has been safely saved to the database. Ashwini will be in touch soon.",
            "id": str(result.inserted_id),
            "timestamp": now_utc.isoformat()
        }
    except Exception as exc:
        logger.error(f"Failed to insert contact document: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving your message to the database. Please try emailing ashwinisamaneti@gmail.com."
        )
