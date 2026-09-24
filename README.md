# EduBridge SA

**Bridging the digital skills gap, one learner at a time.**

EduBridge SA is a low-bandwidth-first digital learning platform designed for
South Africans who face financial, geographic, connectivity or resource
barriers to formal IT training. Instead of "here are 500 videos, good luck",
learners choose a career goal and receive a structured, level-by-level
pathway with lessons, quizzes, progress tracking and badges.

## Problem

A learner in a township or rural community may have a smartphone but no
laptop, expensive limited data, no computer lab, no money for formal courses,
and no mentor. Existing free content is unstructured and hard to trust.

## Proposed Solution

A structured learning journey:

```
Learner joins → chooses career goal → receives pathway
→ completes lessons → takes quizzes → earns badges
→ builds a skills profile → gets pointed toward opportunities
```

Designed **low-data first**: text-first lessons, minimal JavaScript,
no autoplay video, responsive mobile UI, optional downloadable resources.

## Target Users

- Learners seeking free digital skills (computer literacy → cloud)
- Instructors delivering community classes
- Administrators monitoring platform usage

## Features (v1.0 — Phases 1 + 3)

- Landing page (mobile-first, low-data)
- Registration / Login (JWT authentication)
- Learner dashboard with skills profile and progress bars
- Career pathways: IT Support, Cloud Practitioner, Junior Developer,
  Cybersecurity Analyst, Digital Entrepreneur
- Courses → modules → lessons
- Quizzes with 70% pass mark and retry
- Lesson completion + progress tracking
- Badges for completed courses
- **15-question digital skills assessment** → skill bars per category +
  personalised pathway recommendation
- **Personalised next lesson** along your chosen pathway
- **Certificates auto-issued** when a course is fully completed and quizzed
- **Opportunities board**: learnerships, YES programmes, internships,
  entry-level jobs, free certifications
- Role-based access control (learner / admin)
- Admin stats endpoint (learners, courses, lessons, quiz results)

## Architecture

```
        USERS
          │
          ▼
   ┌──────────────┐
   │  Next.js Web  │          Phase 1: local
   └──────┬───────┘
          │  JSON / JWT
          ▼
   ┌──────────────┐     ┌──────────────┐
   │  FastAPI      │────▶│  SQLite /     │
   │  (Python)     │     │  PostgreSQL   │
   └──────────────┘     └──────────────┘

Phase 2 (AWS):
CloudFront → API Gateway → Lambda (FastAPI) → RDS PostgreSQL
                │                │
                S3          CloudWatch + IAM
                │
           Route 53 (edubridge.co.za)
```

## AWS Services (roadmap)

| Service | Purpose |
|---------|---------|
| S3 | Static frontend + learning resources |
| RDS | PostgreSQL (learners, courses, progress) |
| Lambda | FastAPI backend handlers |
| API Gateway | HTTP API in front of Lambda |
| IAM | Least-privilege access control |
| CloudWatch | Logs, metrics, monitoring |
| CloudFront | CDN for low-latency, low-cost delivery |
| Route 53 | DNS for edubridge.co.za |
| EC2 | Optional full-stack hosting |
| VPC / Security Groups | Network isolation |

## Technology Stack

- **Frontend:** Next.js 14 (React), plain CSS — no UI framework bloat
- **Backend:** Python 3.11 + FastAPI
- **Database:** SQLite locally → PostgreSQL / Amazon RDS (`DATABASE_URL`)
- **Auth:** JWT + PBKDF2 password hashing + RBAC
- **Version control:** Git / GitHub

## Database Design

Tables: `users`, `pathways`, `pathway_levels`, `courses`, `modules`,
`lessons`, `quiz_questions`, `progress`, `quiz_results`, `certificates`,
`assessment_questions`, `assessment_results`, `job_opportunities`
— see `database/schema.sql` and `backend/app/models.py`.

## Security

- PBKDF2-SHA256 password hashing (100k iterations, per-user salt)
- JWT bearer tokens with expiry
- Role-based authorization (`learner`, `admin`)
- CORS restricted to known origins
- Secrets via environment variables (`.env`)
- Phase 2: IAM least privilege, security groups, encryption at rest/in transit

## Installation

Prerequisites: Python 3.11+, Node 18+

```bash
git clone https://github.com/<you>/edubridge-sa.git
cd edubridge-sa
```

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
python -m app.seed            # seed courses, pathways, admin user
uvicorn app.main:app --reload --port 8000
```

API docs: http://127.0.0.1:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev                   # http://localhost:3000
```

Optional: create `frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### Default admin

```
email:    admin@edubridge.co.za
password: Admin123!          # CHANGE IN PRODUCTION
```

### Switch to PostgreSQL

Set `DATABASE_URL=postgresql+psycopg://user:pass@host/edubridge` in
`backend/.env` — no code changes required.

## Running Locally

1. Start backend on :8000
2. Start frontend on :3000
3. Register a learner, choose a pathway, complete lessons and quizzes

## Deployment (Phase 2 — AWS)

Planned pipeline: frontend → S3 + CloudFront; backend → Lambda + API
Gateway; database → RDS PostgreSQL; secrets → environment/IAM;
monitoring → CloudWatch; domain → Route 53.

## Future Improvements

- Learning centres directory (community labs)
- PWA offline mode: download lessons, study offline, sync progress
- Instructor role and admin web dashboard UI
- Digital marketing / data analyst pathways with dedicated content

## Social Impact

EduBridge targets the real barriers to digital skills in South Africa:
data cost, device access, geography and lack of guidance. It provides
**skills guidance and training content — it does not guarantee employment.**

## Screenshots

<img width="910" height="475" alt="image" src="https://github.com/user-attachments/assets/f067d757-57b7-43b5-8a13-ac16195c79ce" />


## License

MIT — see [LICENSE](LICENSE).
