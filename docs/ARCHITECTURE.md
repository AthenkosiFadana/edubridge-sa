# EduBridge SA — Architecture (Phase 1 → Phase 2)

## Phase 1 (current): Local MVP

```
 Browser (Next.js, ~96 kB JS)
        │  fetch + JWT
        ▼
 FastAPI (Python 3.11)
        │
        ▼
 SQLite  (edubridge.db)  ── later: PostgreSQL / Amazon RDS
```

### Backend API

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | /auth/register | — | Create learner account |
| POST | /auth/login | — | Get JWT |
| GET | /auth/me | user | Current user |
| GET | /courses | — | List courses |
| GET | /courses/{id} | — | Course + modules + lessons |
| GET | /pathways | — | List career pathways |
| GET | /pathways/{id} | — | Pathway levels |
| POST | /me/pathway | user | Choose pathway |
| GET | /me/lessons/{id}/content | user | Lesson + quiz questions |
| POST | /me/lessons/complete | user | Mark lesson done |
| POST | /me/quizzes/submit | user | Score quiz (pass ≥ 70%) |
| GET | /me/progress | user | Completed lessons |
| GET | /me/profile | user | Skills profile + badges + certs + next lesson |
| GET | /me/next-lesson | user | Personalised next lesson along pathway |
| GET | /me/certificates | user | Earned certificates (auto-issued on completion) |
| GET | /assessment/questions | — | 15-question digital skills assessment |
| POST | /assessment/submit | user | Score assessment → skill bars + pathway recommendation |
| GET | /opportunities | — | Learnerships, YES, internships, jobs, certifications |
| GET | /admin/stats | admin | Platform statistics |
| GET | /admin/users | admin | User list |

### Certificate rules

A certificate is auto-issued when a learner has:

1. Completed **every lesson** in the course, and
2. Passed (≥ 70%) the quiz on **every lesson that has one**.

### Security model

1. Passwords hashed with PBKDF2-SHA256 (100k iterations, random salt)
2. JWT (HS256) with 7-day expiry, signed by `SECRET_KEY`
3. `require_admin` dependency enforces RBAC on admin routes
4. CORS allow-list via `cors_origins`

## Phase 2: AWS deployment

```
 USERS
   │
   ▼
 Route 53 (edubridge.co.za)
   │
   ▼
 CloudFront  ──────────────▶  S3 (frontend static assets)
   │
   ▼ (dynamic /api/*)
 API Gateway ──▶ Lambda (FastAPI container) ──▶ RDS PostgreSQL
                     │                │
                  IAM            CloudWatch (logs/metrics)
                     │
              Security Groups (least privilege)
```

### re/Start skill mapping

| re/Start skill | Where it appears in EduBridge |
|-----------------|-------------------------------|
| Linux | EC2/Lambda runtime, environment management |
| Python | FastAPI backend, seed scripts |
| Networking | VPC, subnets, security groups, Route 53 |
| Security | JWT, RBAC, IAM, encryption, HTTPS |
| Databases | RDS PostgreSQL schema (database/schema.sql) |
| AWS Cloud | Overall Phase 2 architecture |
| Git/GitHub | Version control, PR workflow |
| EC2 | Alternative full-stack hosting |
| S3 | Frontend hosting + resource storage |
| IAM | Least-privilege execution roles |
| Lambda | Serverless API handlers |
| API Gateway | HTTP front door for the API |
| CloudWatch | Structured logs, alarms |
| Auto Scaling | Lambda concurrency / RDS scaling |
| CloudFront | CDN for low-bandwidth delivery |

## Low-data design decisions

- Lesson content is text/markdown — kilobytes, not megabytes
- No autoplay video; video links are opt-in
- Single CSS file, no UI framework
- First Load JS ≈ 96 kB shared across pages
- Static course pages cacheable via CloudFront in Phase 2
- Future: PWA with offline lesson packs + progress sync
