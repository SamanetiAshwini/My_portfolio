# Ashwini Samaneti — Premium Interactive Developer Portfolio

Production-minded personal portfolio and systems showcase for **Samaneti Ashwini**, B.Tech in Artificial Intelligence graduate and Python Full Stack Developer.

---

## 🌟 Overview & Highlights

- **Visual Identity**: Dark Midnight editorial theme with Electric Violet (`#8B5CF6`), Vibrant Cyan (`#06B6D4`), subtle magenta gradients, fine gridlines, glassmorphism, and responsive typography.
- **Full-Stack Architecture**: Clean, framework-free frontend (HTML5, Vanilla CSS, Vanilla JavaScript) powered by a high-performance **FastAPI** backend and **MongoDB Atlas** database connectivity.
- **Three Core Resume Projects**:
  1. **CodeFoundry** — Software Engineering Readiness & Simulation Platform with isolated Docker sandboxes and zero-network execution.
  2. **SkillTrack** — Smart Learning & Career Progress Platform with role-based permissions, Django ORM, Redis, and Celery asynchronous queues.
  3. **SMRITI** — AI-Powered College Assistant Robot with OpenCV facial recognition, emotion detection, Raspberry Pi runtime, and ChatGPT API.
- **Explore Ashwini Chatbot**: Floating portfolio knowledge assistant answering questions regarding skills, education, projects, certifications, and contact details.
- **Database & Persistence**: Synchronous PyMongo operations inside synchronous FastAPI endpoints (`def`) to ensure non-blocking thread-pool execution. Includes anti-spam honeypot, input sanitization, and honest error handling when database credentials are not configured.
- **Verified Credentials**: Real education details (VJIT B.Tech AI, CGPA 8.34/10), verified certifications (AWS, Cisco, IBM, Hexart, Infosys), and actual downloadable resume (`/static/docs/Samaneti_Ashwini_Resume.pdf`).

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, Modern CSS3 (CSS Variables, Flexbox/Grid, Glassmorphism), Vanilla JavaScript (ES6+), Fetch API |
| **Backend** | Python 3.10+, FastAPI, Pydantic v2, Uvicorn |
| **Database** | MongoDB Atlas (`ashwini_portfolio`), PyMongo 4.x, dnspython |
| **Containerization & Tools** | Docker, Git, Redis, Celery (Architecture), VS Code |

---

## 📁 Project Structure

```
portfolio_fastapi/
├── main.py                     # FastAPI entry point, static asset mounting, lifecycle & route inclusion
├── database.py                 # PyMongo client singleton, connection health checks, index management
├── models.py                   # Verified source-of-truth project data & specifications
├── schemas.py                  # Pydantic v2 validation models (Contact, Projects, Health, Chat)
├── routes/
│   ├── __init__.py
│   └── api.py                  # REST API routes: /api/health, /api/projects, /api/projects/{slug}, /api/chat
├── services/
│   ├── __init__.py
│   ├── project_service.py      # Project filtering, search, and MongoDB seeding logic
│   ├── contact_service.py      # Contact validation, spam honeypot, and MongoDB persistence
│   └── chatbot_service.py      # Deterministic resume Q&A knowledge engine
├── static/
│   ├── css/
│   │   └── style.css           # Design tokens, midnight palette, animations, and media queries
│   ├── js/
│   │   ├── app.js              # Theme switcher, constellation canvas, modal controller, search filter
│   │   ├── chatbot.js          # Interactive floating chatbot client & suggestion chips
│   │   └── contact.js          # Contact form client-side validation and fetch submission
│   ├── images/
│   │   ├── avatar.svg          # Custom initials monogram badge with glowing orbital rings
│   │   ├── project-codefoundry.svg # Docker sandbox & test runner architecture diagram
│   │   ├── project-skilltrack.svg  # Role-based LMS & Celery queue architecture diagram
│   │   └── project-smriti.svg      # OpenCV camera HUD & speech synthesis diagram
│   └── docs/
│       └── Samaneti_Ashwini_Resume.pdf # Official downloadable resume PDF
├── templates/
│   └── index.html              # Semantic HTML5 single-page application
├── .env.example                # Environment variable documentation & template
├── .gitignore                  # Prevents secrets, virtual environments, and caches from git
├── requirements.txt            # Python production dependencies
└── README.md                   # System documentation & setup guide
```

---

## 🚀 Setup & Local Execution

### 1. Prerequisites
- Python 3.10 or higher installed
- (Optional) MongoDB Atlas free cluster connection string

### 2. Activate Virtual Environment
On Windows (PowerShell):
```powershell
.\venv\Scripts\activate
```
On macOS / Linux:
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Open `.env` and set your MongoDB Atlas connection string:
```env
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.example.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=ashwini_portfolio
JWT_SECRET=your_secret_key_here
CONTACT_EMAIL=ashwinisamaneti@gmail.com
GITHUB_URL=
LINKEDIN_URL=
```
> **Note**: If `MONGODB_URI` is left blank, the portfolio application runs normally in unverified database mode. All project views, chatbot questions, and UI interactions work seamlessly, while contact form submissions report that database connectivity is unverified rather than showing fake success.

### 5. Launch the FastAPI Application
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 6. Explore the Application
- **Interactive Portfolio Website**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **API Health Check**: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

---

## 📡 API Endpoint Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the interactive portfolio frontend (or JSON if `Accept: application/json`) |
| `GET` | `/api/health` | Health status of API and MongoDB Atlas connectivity |
| `GET` | `/api/projects` | List projects with optional `?technology=` and `?search=` filters |
| `GET` | `/api/projects/{slug}` | In-depth project specifications, architecture, and contributions |
| `POST` | `/contact` | Validates and stores inquiry in MongoDB `contacts` collection |
| `POST` | `/api/contact` | Alias endpoint for contact inquiries |
| `POST` | `/api/chat` | Queries the portfolio knowledge assistant |

---

## 🧪 Testing the Application

### 1. Test API Health
```bash
curl http://127.0.0.1:8000/api/health
```

### 2. Test Project Filtering
```bash
curl "http://127.0.0.1:8000/api/projects?technology=Docker"
```

### 3. Test Contact Submission (Validation & Persistence)
```bash
curl -X POST http://127.0.0.1:8000/contact \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Maya Sharma\", \"email\": \"maya@example.com\", \"subject\": \"Collaboration\", \"message\": \"I would like to discuss a Python engineer position with you.\"}"
```

---

## 🔒 Security Best Practices

1. **Synchronous Thread-Pool PyMongo Calls**: Endpoint handlers are declared with `def` rather than `async def`, allowing FastAPI to dispatch synchronous database calls to an internal worker thread pool, preventing event-loop stalls.
2. **Anti-Spam Honeypot Trap**: Invisible field `website` silently captures automated bot submissions.
3. **Pydantic Validation**: Sanitizes and enforces length bounds on all user inputs.
4. **Environment Isolation**: `.env` is listed in `.gitignore` to prevent credential exposure.
5. **No Fake Success Reporting**: Submissions explicitly notify the user if database connectivity is unavailable and provide direct email fallbacks.
