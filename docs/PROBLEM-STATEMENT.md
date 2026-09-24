# EduBridge SA — Problem Statement & Requirements (v1.0)

## Problem

Millions of South Africans face barriers to digital skills training:

- Smartphone but no laptop
- Expensive, limited mobile data
- No access to computer laboratories
- No money for formal IT courses
- No knowledge of where to start
- Hard to find trustworthy free learning material
- No mentor to guide them
- Difficulty translating digital skills into employment

Existing options say: *"Here are 500 YouTube videos. Good luck."*

## Solution

EduBridge SA provides a **structured, low-bandwidth-first learning journey**:

```
Learner joins → chooses career goal → receives learning pathway
→ completes lessons → does practical activities → takes quizzes
→ earns badges → builds a skills profile → gets directed toward opportunities
```

## Target Users

| User | Needs |
|------|-------|
| Learner (township/rural/urban) | Free, structured, data-light digital skills training |
| Instructor | Tools to deliver and track learning |
| Admin | Platform oversight, analytics, content management |

## Career Pathways (Phase 3+)

IT Support · Software Development · Cloud Computing · Cybersecurity ·
Data · Digital Marketing · Office Administration · Digital Entrepreneurship

## MVP Requirements (Phase 1) — MUST HAVE

1. Landing page (low-data, mobile-first)
2. Registration / Login / Logout (JWT authentication)
3. Learner dashboard
4. Browse courses → modules → lessons
5. Lesson completion + progress tracking
6. Quizzes with scoring
7. Learning pathway selection ("I want to become a…")
8. Role-based access: learner / admin
9. Seed data: real pathways, courses, lessons, quizzes

### MVP Requirements — MUST NOT

- No autoplay video, no heavy JS frameworks on lesson pages
- No guarantee of employment language (skills guidance only)
- No paid tiers in v1.0

## Non-functional Requirements

| Requirement | Target |
|-------------|--------|
| Bandwidth | Text-first; pages usable on 3G/limited data |
| Mobile | Responsive, works on low-end smartphones |
| Performance | API responses < 300ms locally |
| Security | Hashed passwords, JWT auth, RBAC, HTTPS in prod |
| Portability | Local SQLite → Amazon RDS PostgreSQL via `DATABASE_URL` |
| Database | Relational (users, courses, progress, quizzes) |

## AWS re/Start Mapping

| re/Start skill | EduBridge implementation |
|-----------------|--------------------------|
| Linux | Host/manage application environments |
| Python | FastAPI backend/API |
| Networking | VPC architecture (Phase 2) |
| Security | JWT, RBAC, IAM, encryption (Phase 2) |
| Databases | Learners, courses, progress, quizzes → RDS |
| AWS Cloud | Overall infrastructure |
| Git/GitHub | Version control |
| EC2/S3/Lambda/API Gateway | Hosting, storage, serverless (Phase 2) |
| CloudWatch | Monitoring/logging (Phase 2) |
| Route 53 / CloudFront | Domain + CDN (Phase 2) |

## Phases

- **Phase 1 (this repo, v1.0):** Landing, auth, dashboard, courses/modules/lessons, quizzes, progress
- **Phase 2:** Deploy to AWS (CloudFront, API Gateway, Lambda, RDS, S3, IAM, CloudWatch)
- **Phase 3:** Skill assessment, personalised pathways, skills profile, certificates, opportunities
- **Phase 4:** Community learning centres directory
- **Phase 5:** Offline/low-connectivity PWA sync

## Social Impact Note

EduBridge provides **skills guidance and learning content**. It does not
guarantee employment. Opportunity listings (learnerships, YES programmes,
internships) are informational.
