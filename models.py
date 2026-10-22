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
        "title": "Saarthi: A Smriti",
        "tagline": "Knowledge-Driven AI Robot for Multimodal Interaction & Assistance · Springer CIGAI 2026",
        "category": "Multimodal AI & Robotics (Springer Published)",
        "technologies": [
            "Python (Multi-threaded)",
            "Raspberry Pi 4 Model B",
            "Cloud LLMs (Gemini / GPT)",
            "Whisper Speech Recognition",
            "SSD1306 OLED Animation",
            "TB6612FNG Motor Driver",
            "IR Flame Safety Sensor",
            "Flask Web Interface"
        ],
        "problem": (
            "Modern service and campus environments require low-cost, scalable robotic platforms capable of "
            "natural spoken dialogue, expressive emotional feedback, autonomous or remote navigation, and "
            "continuous environmental safety hazard monitoring without high latency or excessive hardware costs."
        ),
        "solution": (
            "Saarthi: A Smriti is an AI-enabled multimodal interactive robotic system presented at Springer CIGAI 2026. "
            "Built on a Raspberry Pi 4 Model B running a multi-threaded Python framework, it integrates cloud LLMs for "
            "contextual dialogue, an SSD1306 OLED display for synchronized facial expression states ('Listening' / 'Thinking'), "
            "TB6612FNG motor control with web-based teleoperation, and active-high infrared flame sensing for <0.5s emergency alerts."
        ),
        "features": [
            "Published Research: Presented at the 2nd International Conference on Computational Intelligence & Generative AI (CIGAI 2026, Springer Publishing Partner).",
            "Multi-Threaded Architecture: Independent concurrent threads for audio perception, LLM conversational intelligence, motor actuation, and high-priority safety monitoring.",
            "Multimodal Expressiveness: SSD1306 OLED animated eyes visual feedback synced with text-to-speech voice responses.",
            "Voice-to-Voice Pipeline: USB microphone audio digitization with Whisper speech-to-text, LLM context reasoning, and loudspeaker audio output.",
            "Real-Time Environmental Safety: Continuous flame sensor monitoring with immediate motor halt, buzzer trigger, and verbal warning within <0.5 seconds.",
            "Documented Experimental Performance: <1s interaction response latency, 98.5% interaction success rate, 97% directional motor accuracy, and 6+ hours continuous system uptime."
        ],
        "contributions": [
            "Co-authored peer-reviewed research paper 'Saarthi: A Smriti – A Knowledge-Driven AI Robot for Intelligent Communication and Assistance' presented at Springer CIGAI 2026.",
            "Engineered the multi-threaded Python framework on Raspberry Pi 4 Model B coordinating speech capture, cloud LLM requests, and actuator threads.",
            "Implemented the real-time safety monitor thread for instant flame detection, fail-safe motor interruption, and verbal emergency alerts.",
            "Integrated SSD1306 OLED animated facial states and web-based motor control interface for responsive indoor service assistance."
        ],
        "order": 3,
        "featured": True,
        "paper_url": "/static/docs/Saarthi_Smriti_Research_Paper.pdf",
        "certificate_url": "/static/images/smriti-certificate.jpg",
        "github_url": None,
        "demo_url": None,
        "image_svg": "/static/images/smriti-robot-top.jpg"
    }
]
