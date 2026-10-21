"""
API router for Ashwini Samaneti's Portfolio.
Endpoints are defined with synchronous `def` handlers to ensure safe,
non-blocking execution on FastAPI's thread pool when accessing PyMongo.
"""

from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query, Request, status
from schemas import (
    ContactCreate,
    ContactResponse,
    ProjectSchema,
    HealthResponse,
    ChatRequest,
    ChatResponse
)
from database import check_db_connection
from services.project_service import get_all_projects, get_project_by_id_or_slug
from services.contact_service import handle_contact_submission
from services.chatbot_service import process_chat_message

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """
    Returns API and database connectivity status without exposing sensitive credentials.
    """
    is_connected, db_message = check_db_connection()
    return {
        "status": "ok" if is_connected else "degraded",
        "api": "healthy",
        "version": "1.0.0",
        "database_connected": is_connected,
        "database_message": db_message,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/projects", response_model=List[ProjectSchema], tags=["Projects"])
def list_projects(
    technology: Optional[str] = Query(None, description="Filter projects by technology (e.g. Django, Docker, OpenCV)"),
    search: Optional[str] = Query(None, description="Search keyword in title, tagline, or features")
):
    """
    List featured portfolio projects with optional technology and keyword filtering.
    """
    return get_all_projects(technology=technology, search=search)


@router.get("/projects/{slug_or_id}", response_model=ProjectSchema, tags=["Projects"])
def get_project(slug_or_id: str):
    """
    Retrieve in-depth details for a single project by slug or ID.
    """
    project = get_project_by_id_or_slug(slug_or_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{slug_or_id}' was not found."
        )
    return project


@router.post("/contact", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, tags=["Contact"])
def submit_contact(contact: ContactCreate, request: Request):
    """
    Validate and store a new contact submission in MongoDB.
    Includes spam honeypot validation and safe error reporting.
    """
    client_ip = request.client.host if request.client else "unknown"
    return handle_contact_submission(contact, client_ip=client_ip)


@router.post("/chat", response_model=ChatResponse, tags=["Chatbot"])
def chat_query(query: ChatRequest):
    """
    Process queries through Ashwini's portfolio knowledge assistant.
    Returns verified responses matching resume and project specifications.
    """
    result = process_chat_message(query.message)
    return {
        "reply": result["reply"],
        "intent": result["intent"],
        "suggested_prompts": result.get("suggested_prompts", [])
    }
