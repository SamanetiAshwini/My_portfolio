"""
Chatbot service providing deterministic, verified answers based on Ashwini's resume and portfolio.
Transparently communicates answers without claiming external LLM capabilities unless connected.
"""

from typing import Dict, Any, List
import re

PORTFOLIO_KNOWLEDGE = {
    "codefoundry": {
        "patterns": [r"code\s*foundry", r"\bsandbox(ed)?\b", r"\breadiness\b"],
        "reply": (
            "**CodeFoundry** is a Software Engineering Readiness & Simulation Platform built with "
            "Django 5.2, DRF, PostgreSQL, Redis, React, and Docker.\n\n"
            "• Purpose: A repository-style coding platform where candidates solve bug-fixing, feature-development, "
            "API, security, and code-review challenges.\n"
            "• Workflow: Challenge selection -> workspace -> submission -> isolated Docker execution -> automated test evaluation -> scoring.\n"
            "• Security: Sandboxed Docker containers with CPU/memory limits, no-network execution, and path traversal validation.\n"
            "• Ashwini's Role: Designed backend services for authentication, challenge management, and sandboxed Docker runners."
        ),
        "prompts": ["Tell me about SkillTrack", "Tell me about SMRITI", "View all projects"]
    },
    "skilltrack": {
        "patterns": [r"skill\s*track", r"\blms\b", r"\bcareer\s*progress\b", r"\bcelery\b"],
        "reply": (
            "**SkillTrack** is a Smart Learning & Career Progress Platform built with Django, DRF, "
            "PostgreSQL, Redis, Celery, and JWT Authentication.\n\n"
            "• Purpose: Role-based platform for Students, Mentors, and Administrators.\n"
            "• Key Features: Course enrollment, modular topic progression, assignment submissions, mentor code reviews, and performance analytics.\n"
            "• Async Architecture: Redis and Celery power background milestone calculations and automated alerts.\n"
            "• Ashwini's Role: Relational schema design with Django ORM, JWT authentication, and REST APIs with filtering, search, and pagination."
        ),
        "prompts": ["Tell me about CodeFoundry", "Tell me about SMRITI", "What are your skills?"]
    },
    "smriti": {
        "patterns": [r"\bsmriti\b", r"\brobot\b", r"\bopencv\b", r"raspberry\s*pi", r"\bemotion\b"],
        "reply": (
            "**SMRITI** is an AI-Powered College Assistant Robot prototype built with Python, OpenCV, "
            "Speech Recognition, Text-to-Speech (TTS), ChatGPT API, and Raspberry Pi.\n\n"
            "• Key Capabilities: Real-time face recognition and facial emotion detection with OpenCV to identify visitors.\n"
            "• Conversational Intelligence: Integrates the ChatGPT API for context-aware responses to campus questions.\n"
            "• Voice Interaction: Speech recognition for query input and speech synthesis for verbal output.\n"
            "• Ashwini's Role: Built the core Python runtime on Raspberry Pi, OpenCV emotion recognition pipeline, and conversational API bridge."
        ),
        "prompts": ["Tell me about your certifications", "Tell me about your education", "Contact Ashwini"]
    },
    "education": {
        "patterns": [r"\beducation\b", r"\bcollege\b", r"\bdegree\b", r"b\.?tech", r"\bvjit\b", r"\buniversity\b", r"\bcgpa\b", r"\bstudy\b", r"\bstudied\b"],
        "reply": (
            "Ashwini's academic journey:\n\n"
            "1. **B.Tech in Artificial Intelligence** (2022 – 2026)\n"
            "   Vidya Jyothi Institute of Technology (VJIT), Hyderabad\n"
            "   CGPA: **8.34 / 10**\n\n"
            "2. **Intermediate (MPC)** (2020 – 2022)\n"
            "   Sri Chaitanya Junior College — **73.1%**\n\n"
            "3. **Secondary Education (10th Grade)** (2020)\n"
            "   Infant Jesus International School — **GPA: 10 / 10**"
        ),
        "prompts": ["What certifications do you hold?", "What projects have you built?", "Download resume"]
    },
    "skills": {
        "patterns": [r"\bskills?\b", r"\btech(nology|nologies)?\b", r"\bstack\b", r"\bpython\b", r"\bfastapi\b", r"\bdjango\b", r"\bdocker\b", r"\bsql\b", r"\bai\b", r"\bml\b"],
        "reply": (
            "Here is Ashwini's technical skill universe:\n"
            "• Languages: Python, SQL\n"
            "• Backend & APIs: Django, Django REST Framework (DRF), FastAPI, Flask, REST APIs, JWT Authentication\n"
            "• Frontend: HTML5, CSS3, JavaScript (Vanilla)\n"
            "• AI / ML: Machine Learning, Deep Learning, NLP, LLMs, Prompt Engineering, RAG, OpenCV\n"
            "• Databases & Tools: PostgreSQL, MySQL, MongoDB, Docker, Git, GitHub, Redis, Celery, Jupyter, VS Code"
        ),
        "prompts": ["Tell me about CodeFoundry", "Tell me about SkillTrack", "Tell me about SMRITI"]
    },
    "certifications": {
        "patterns": [r"\b(certif|credentials|aws|ibm|cisco|pcap|infosys|hexart|hackathon|sih|achieve)\b"],
        "reply": (
            "Ashwini's certifications & achievements:\n\n"
            "• **AWS Academy Graduate**: Machine Learning Foundations — Amazon Web Services (2024)\n"
            "• **PCAP**: Programming Essentials in Python — Cisco Networking Academy / OpenEDG (2023)\n"
            "• **Python for Data Science** (PY0101EN) — IBM (2023)\n"
            "• **AI Foundation / AI Advanced** — Hexart.In (NASSCOM Foundation, Li2, Hexagon) (2024)\n"
            "• **Natural Language Processing** — Infosys Springboard (2025)\n"
            "• **Smart India Hackathon (SIH)**: Developed a Real-Time Vehicle Tracking System (Smart Vehicles theme)\n"
            "• **NIT Warangal**: Attended national program on AI/ML/DL applications"
        ),
        "prompts": ["Tell me about your projects", "What are your skills?", "Contact Ashwini"]
    },
    "contact": {
        "patterns": [r"\b(contact|hire|email|phone|reach|message|talk|interview|opportunity)\b"],
        "reply": (
            "You can reach Ashwini directly through:\n\n"
            "• **Email**: ashwinisamaneti@gmail.com\n"
            "• **Portfolio Contact Form**: Submit the form in the Contact section below\n"
            "• **Location**: Hyderabad, Telangana, India\n"
            "• Open to entry-level Python Software Engineer, Backend Developer, and Full Stack roles!"
        ),
        "prompts": ["Download resume", "What are your core skills?", "Tell me about CodeFoundry"]
    },
    "resume": {
        "patterns": [r"\b(resume|cv|download cv|download resume|curriculum vitae)\b"],
        "reply": (
            "You can download Ashwini's official resume directly via the 'Download Resume' button in the Hero section "
            "or by visiting [/static/docs/Samaneti_Ashwini_Resume.pdf](/static/docs/Samaneti_Ashwini_Resume.pdf). "
            "It highlights her B.Tech in AI, Python full stack development expertise, and project contributions."
        ),
        "prompts": ["What are your core skills?", "Tell me about CodeFoundry", "Contact Ashwini"]
    },
    "about": {
        "patterns": [r"who\s+(are\s+you|is\s+ashwini)", r"\bbio\b", r"\bbackground\b", r"about\s+(yourself|ashwini|you)", r"\bintroduce\b", r"\bprofile\b"],
        "reply": (
            "Samaneti Ashwini is an entry-level Python Full Stack Developer and B.Tech graduate in "
            "Artificial Intelligence from Vidya Jyothi Institute of Technology (VJIT), Hyderabad (CGPA 8.34/10). "
            "She specializes in developing robust backend REST APIs (FastAPI, Django, Flask), database-driven "
            "systems (PostgreSQL, MongoDB, SQL), containerized deployments (Docker), and integrating AI/ML models "
            "(OpenCV, NLP, LLMs, RAG)."
        ),
        "prompts": ["Tell me about CodeFoundry", "What is your tech stack?", "Download resume"]
    },
    "greeting": {
        "patterns": [r"\b(hi|hello|hey|greetings|morning|afternoon|evening|namaste)\b"],
        "reply": (
            "Hello! I am Ashwini's Portfolio Assistant. I can tell you about Ashwini's "
            "technical skills, full-stack & AI projects (CodeFoundry, SkillTrack, SMRITI), "
            "education at VJIT, certifications, or how to get in touch. What would you like to explore?"
        ),
        "prompts": ["What projects have you built?", "What are your core skills?", "Tell me about your education", "How can I contact Ashwini?"]
    }
}


def process_chat_message(user_message: str) -> Dict[str, Any]:
    """
    Processes a visitor query against Ashwini's verified portfolio knowledge base.
    Returns structured reply, intent key, and suggested follow-up prompts.
    """
    clean_msg = user_message.strip().lower()

    for intent, data in PORTFOLIO_KNOWLEDGE.items():
        for pattern in data["patterns"]:
            if re.search(pattern, clean_msg, re.IGNORECASE):
                return {
                    "reply": data["reply"],
                    "intent": intent,
                    "suggested_prompts": data["prompts"]
                }

    # Default fallback
    return {
        "reply": (
            "I'm Ashwini's Portfolio Knowledge Assistant. I don't have information on that specific phrase, "
            "but I can share verified details about Ashwini's software projects (CodeFoundry, SkillTrack, SMRITI), "
            "technical skills in Python, FastAPI & AI, educational background at VJIT, or how to contact her."
        ),
        "intent": "fallback",
        "suggested_prompts": [
            "Tell me about CodeFoundry",
            "What are your core skills?",
            "Tell me about your education",
            "How can I contact Ashwini?"
        ]
    }
