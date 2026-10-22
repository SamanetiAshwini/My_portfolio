"""
Domain models and source-of-truth project data for Ashwini Samaneti.
Contains exact, verified resume details without invented statistics or repositories.
"""

from typing import List, Dict, Any

PROJECTS_DATA: List[Dict[str, Any]] = [
    {
        "id": "proj-codefoundry",
        "slug": "codefoundry",
        "title": "CodeFoundry",
        "tagline": "Software Engineering Readiness & Simulation Platform",
        "category": "Full Stack & Sandboxed Systems",
        "technologies": [
            "Python",
            "Django 5.2",
            "Django REST Framework",
            "PostgreSQL",
            "Redis",
            "React",
            "Docker"
        ],
        "problem": (
            "Software engineering candidates often struggle to demonstrate realistic problem-solving "
            "because traditional assessment platforms focus narrowly on leetcode-style algorithmic puzzles "
            "rather than real-world codebase challenges like bug-fixing, feature integration, database tuning, "
            "and security hardening."
        ),
        "solution": (
            "CodeFoundry is a repository-style practice platform providing comprehensive engineering scenarios. "
            "Candidates clone or open challenge workspaces, fix real issues, run tests inside isolated Docker "
            "sandboxes with strict security boundaries, and receive automated evaluation and structured scorecards."
        ),
        "features": [
            "Repository-style software engineering practice covering bug fixing, feature development, REST APIs, databases, performance, security, testing, code review, and debugging.",
            "End-to-end evaluation lifecycle: challenge selection, repository workspace, submissions, isolated Docker execution, automated test scoring, and progress tracking.",
            "Backend architecture supporting authentication, challenges, submissions, evaluation, skill profiles, achievements, public developer profiles, and recruiter dashboards.",
            "Multi-layer execution security: isolated Docker sandboxes, CPU/memory resource limits, strictly no-network execution, path traversal validation, and server-side evaluation."
        ],
        "contributions": [
            "Architected backend micro-services with Django 5.2 and Django REST Framework for challenge lifecycle, submission pipelines, and candidate scoring profiles.",
            "Engineered secure containerization sandboxes using Docker with zero-network execution and file path validation to prevent untrusted code escape.",
            "Modeled normalized relational schemas in PostgreSQL with Redis caching for rapid challenge state synchronization and session validation."
        ],
        "order": 1,
        "featured": True,
        "github_url": "https://github.com/puppalanagababu/CodeFoundry",
        "demo_url": None,    # Configurable placeholder per specification
        "image_svg": "/static/images/project-codefoundry.svg"
    },
    {
        "id": "proj-skilltrack",
        "slug": "skilltrack",
        "title": "SkillTrack",
        "tagline": "Smart Learning & Career Progress Platform",
        "category": "Web & Backend Systems",
        "technologies": [
            "Python",
            "Django",
            "Django REST Framework",
            "PostgreSQL",
            "Redis",
            "Celery",
            "JWT"
        ],
        "problem": (
            "Educational programs and bootcamps face significant overhead managing fragmented tools for student "
            "learning, module assessments, mentor feedback loops, and job-application tracking across different stages."
        ),
        "solution": (
            "SkillTrack delivers a unified, role-based platform for students, mentors, and administrators. "
            "It structures the complete learning journey from curriculum enrollment and topic milestones to "
            "project evaluations, mentor code reviews, and career readiness dashboards."
        ),
        "features": [
            "Three-tier role-based access control (Students, Mentors, Administrators) with granular permission guards.",
            "Comprehensive learning workflow spanning course enrollments, topic completion, structured assessments, project submissions, mentor feedback loops, and performance analytics.",
            "Asynchronous background task processing with Celery and Redis for automated evaluation triggers and milestone notifications.",
            "Production-ready RESTful APIs with JWT authentication, role-based filtering, search, pagination, and structured error responses."
        ],
        "contributions": [
            "Designed and normalized relational database models with Django ORM and PostgreSQL for users, courses, learning modules, enrollments, assessments, and projects.",
            "Implemented RESTful API endpoints with JWT authentication, permission classes, search, filtering, and pagination.",
            "Integrated Celery task queues with Redis message broker for reliable asynchronous milestone calculations and notification delivery."
        ],
        "order": 2,
        "featured": True,
        "github_url": None,  # Configurable placeholder per specification
        "demo_url": None,    # Configurable placeholder per specification
        "image_svg": "/static/images/project-skilltrack.svg"
    },
    {
        "id": "proj-smriti",
        "slug": "smriti",
        "title": "SMRITI",
        "tagline": "AI-Powered College Assistant Robot",
        "category": "AI, Computer Vision & Robotics",
        "technologies": [
            "Python",
            "OpenCV",
            "Speech Recognition",
            "Text-to-Speech (TTS)",
            "ChatGPT API",
            "Raspberry Pi"
        ],
        "problem": (
            "College departments and engineering campuses require accessible, automated assistance to guide "
            "visitors, answer repetitive departmental inquiries, and deliver an interactive robotic greeting experience."
        ),
        "solution": (
            "SMRITI is a physical AI-powered college assistant robot prototype running on Raspberry Pi. "
            "It combines computer vision for face and emotion detection with LLM conversational intelligence "
            "and natural voice interaction to assist students and visitors in real-time."
        ),
        "features": [
            "Real-time face recognition and facial emotion detection using OpenCV to identify visitors and tailor greetings.",
            "Context-aware collegiate query answering powered by ChatGPT API integration with customized departmental prompts.",
            "Hands-free voice interaction utilizing speech recognition for audio input and text-to-speech for vocal responses.",
            "Embedded Python runtime optimized for Raspberry Pi hardware and low-latency audio/visual processing."
        ],
        "contributions": [
            "Developed the core Python event-driven architecture and device runtime on Raspberry Pi.",
            "Implemented OpenCV facial detection, feature extraction, and emotion classification pipelines.",
            "Integrated the ChatGPT API with structured prompting to supply collegiate guidance and department answers.",
            "Configured bidirectional speech-to-text and text-to-speech pipelines for seamless verbal communication."
        ],
        "order": 3,
        "featured": True,
        "github_url": None,  # Configurable placeholder per specification
        "demo_url": None,    # Configurable placeholder per specification
        "image_svg": "/static/images/project-smriti.svg"
    }
]
