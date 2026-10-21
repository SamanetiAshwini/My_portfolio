"""
Ashwini Samaneti — Premium Interactive Developer Portfolio
FastAPI Application Entry Point.
Serves interactive editorial frontend, REST APIs, MongoDB connectivity, and Swagger documentation at /docs.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import init_indexes, check_db_connection
from schemas import ContactCreate, ContactResponse
from routes.api import router as api_router
from services.contact_service import handle_contact_submission
from services.project_service import seed_projects_if_needed

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle management:
    Initializes database indexes and seeds default project records if MongoDB is connected.
    """
    # Initialize indexes and check DB safely
    try:
        init_indexes()
        seed_projects_if_needed()
    except Exception as exc:
        print(f"[Startup Warning] Non-blocking DB initialization note: {exc}")
    yield


app = FastAPI(
    title="Ashwini Samaneti — Portfolio & Systems API",
    description=(
        "Production-minded portfolio backend for Samaneti Ashwini, B.Tech in Artificial Intelligence "
        "and Python Full Stack Developer. Features MongoDB Atlas persistence, project exploration, "
        "and portfolio assistant endpoints."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS for standard web security compliance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include the modular API router under /api
app.include_router(api_router, prefix="/api")


# Preserved and upgraded root endpoint: Serves portfolio UI to browsers and JSON to API clients
@app.get("/", tags=["Frontend"])
def home(request: Request):
    """
    Serves the interactive portfolio frontend application.
    If the caller explicitly requests application/json, returns the API welcome payload.
    """
    accept = request.headers.get("accept", "")
    if "application/json" in accept and "text/html" not in accept:
        return JSONResponse(content={
            "message": "Welcome to Ashwini Samaneti's Developer Portfolio API",
            "title": "Python Full Stack Developer | AI Enthusiast",
            "docs": "/docs",
            "api_health": "/api/health",
            "projects": "/api/projects"
        })

    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(template_path):
        return FileResponse(template_path, media_type="text/html")
    return HTMLResponse("<h1>Ashwini Samaneti Portfolio</h1><p>Frontend template is loading...</p>")


@app.get("/robots.txt", include_in_schema=False)
def robots_txt():
    """Serves robots.txt for search engine crawlers."""
    path = os.path.join(static_dir, "robots.txt")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/plain")
    return HTMLResponse("User-agent: *\nAllow: /", media_type="text/plain")


@app.get("/sitemap.xml", include_in_schema=False)
def sitemap_xml():
    """Serves XML sitemap for SEO."""
    path = os.path.join(static_dir, "sitemap.xml")
    if os.path.exists(path):
        return FileResponse(path, media_type="application/xml")
    return HTMLResponse("<urlset></urlset>", media_type="application/xml")



# Preserved top-level POST /contact endpoint from the initial FastAPI implementation,
# upgraded with robust Pydantic validation and MongoDB Atlas persistence.
@app.post("/contact", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, tags=["Contact"])
def submit_contact_root(contact: ContactCreate, request: Request):
    """
    Submits a contact inquiry to MongoDB Atlas. Preserves the initial /contact endpoint URL.
    """
    client_ip = request.client.host if request.client else "unknown"
    return handle_contact_submission(contact, client_ip=client_ip)


@app.get("/api", tags=["General"])
def api_root():
    """
    API discovery endpoint.
    """
    return {
        "message": "Ashwini Samaneti Portfolio API v1.0.0",
        "author": "Samaneti Ashwini",
        "role": "Python Full Stack Developer | AI Enthusiast",
        "documentation": "/docs",
        "routes": {
            "health": "/api/health",
            "projects": "/api/projects",
            "project_detail": "/api/projects/{slug_or_id}",
            "contact": "/contact",
            "chatbot": "/api/chat"
        }
    }
