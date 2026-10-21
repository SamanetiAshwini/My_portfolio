"""
Pydantic validation schemas for API requests, responses, and data contracts.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator
import re


class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80, description="Full name of sender")
    email: str = Field(..., max_length=100, description="Valid email address")
    subject: Optional[str] = Field(default="", max_length=150, description="Optional subject")
    message: str = Field(..., min_length=10, max_length=3000, description="Message content")
    # Anti-spam honeypot field (hidden from real users, bots often fill it)
    website: Optional[str] = Field(default=None, description="Spam honeypot trap")

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, v: str) -> str:
        clean = v.strip()
        if len(clean) < 2:
            raise ValueError("Name must be at least 2 characters.")
        return clean

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean = v.strip().lower()
        # Basic RFC 5322 compatible pattern
        email_regex = r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$"
        if not re.match(email_regex, clean):
            raise ValueError("Please provide a valid email address.")
        return clean

    @field_validator("message")
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        clean = v.strip()
        if len(clean) < 10:
            raise ValueError("Message must be at least 10 characters.")
        return clean


class ContactResponse(BaseModel):
    success: bool
    message: str
    id: Optional[str] = None
    timestamp: Optional[str] = None


class ProjectSchema(BaseModel):
    id: str
    slug: str
    title: str
    tagline: str
    category: str
    technologies: List[str]
    problem: str
    solution: str
    features: List[str]
    contributions: List[str]
    order: int = 1
    featured: bool = True
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    image_svg: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    api: str
    version: str
    database_connected: bool
    database_message: str
    timestamp: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)


class ChatResponse(BaseModel):
    reply: str
    intent: str
    suggested_prompts: List[str] = Field(default_factory=list)
