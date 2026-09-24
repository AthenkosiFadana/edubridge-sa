import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

# Use a fresh test DB before app import
_test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["DATABASE_URL"] = f"sqlite:///{_test_db.name}"

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402
from app import seed  # noqa: E402

Base.metadata.create_all(bind=engine)
seed.seed()

client = TestClient(app)


def register(name="Test User", email="t@example.com", password="Password123!"):
    r = client.post(
        "/auth/register",
        json={"name": name, "email": email, "password": password, "location": "Cape Town"},
    )
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_register_login_me():
    headers = register(email="me@example.com")
    me = client.get("/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["email"] == "me@example.com"

    bad = client.post("/auth/login", json={"email": "me@example.com", "password": "wrongpass1"})
    assert bad.status_code == 401

    ok = client.post("/auth/login", json={"email": "me@example.com", "password": "Password123!"})
    assert ok.status_code == 200


def test_duplicate_email_rejected():
    register(email="dup@example.com")
    r = client.post(
        "/auth/register",
        json={"name": "Dup", "email": "dup@example.com", "password": "Password123!"},
    )
    assert r.status_code == 409


def test_catalog_endpoints():
    courses = client.get("/courses").json()
    assert len(courses) >= 5

    detail = client.get(f"/courses/{courses[0]['id']}")
    assert detail.status_code == 200
    assert detail.json()["modules"]

    pathways = client.get("/pathways").json()
    assert any(p["title"] == "IT Support Technician" for p in pathways)

    p1 = client.get(f"/pathways/{pathways[0]['id']}").json()
    assert p1["levels"], "pathway must have levels"


def test_lesson_quiz_progress_flow():
    headers = register(email="flow@example.com")

    # choose pathway
    r = client.post("/me/pathway", headers=headers, json={"pathway_id": 1})
    assert r.status_code == 200

    # first lesson of first course
    courses = client.get("/courses").json()
    course = client.get(f"/courses/{courses[0]['id']}").json()
    lesson_id = course["modules"][0]["lessons"][0]["id"]

    # lesson content includes quiz but not the correct answers
    lesson = client.get(f"/me/lessons/{lesson_id}/content", headers=headers).json()
    assert lesson["quiz_questions"]
    assert "correct_answer" not in lesson["quiz_questions"][0]

    # complete lesson
    r = client.post("/me/lessons/complete", headers=headers, json={"lesson_id": lesson_id})
    assert r.status_code == 201

    # idempotent
    r2 = client.post("/me/lessons/complete", headers=headers, json={"lesson_id": lesson_id})
    assert r2.status_code in (200, 201)

    # submit quiz using correct answers from the test DB
    from sqlalchemy import select

    from app.database import SessionLocal
    from app.models import QuizQuestion

    db = SessionLocal()
    try:
        rows = db.scalars(
            select(QuizQuestion).where(QuizQuestion.lesson_id == lesson_id)
        ).all()
        answers = {str(q.id): q.correct_answer for q in rows}
        correct_set = set(answers.values())
    finally:
        db.close()

    res = client.post(
        "/me/quizzes/submit", headers=headers, json={"lesson_id": lesson_id, "answers": answers}
    ).json()
    assert res["score"] == res["total"]
    assert res["passed"] is True

    # wrong answers (unless all correct answers happen to be identical)
    qids = [q["id"] for q in lesson["quiz_questions"]]
    wrong_choice = "c" if "c" not in correct_set else "d"
    wrong = {str(qid): wrong_choice for qid in qids}
    res2 = client.post(
        "/me/quizzes/submit", headers=headers, json={"lesson_id": lesson_id, "answers": wrong}
    ).json()
    assert res2["passed"] is False or res2["score"] < res2["total"]

    # profile reflects progress
    profile = client.get("/me/profile", headers=headers).json()
    assert profile["lessons_completed"] >= 1
    assert profile["pathway"]["title"] == "IT Support Technician"
    assert profile["quizzes_passed"] >= 1

    progress = client.get("/me/progress", headers=headers).json()
    assert any(p["lesson_id"] == lesson_id for p in progress)


def test_auth_required():
    assert client.get("/me/profile").status_code in (401, 403)
    assert client.post("/me/lessons/complete", json={"lesson_id": 1}).status_code in (401, 403)


def test_admin_rbac():
    # learner cannot access admin
    learner = register(email="learner-rbac@example.com")
    assert client.get("/admin/stats", headers=learner).status_code == 403

    # no token
    assert client.get("/admin/stats").status_code == 401

    # seeded admin can
    login = client.post(
        "/auth/login", json={"email": "admin@edubridge.co.za", "password": "Admin123!"}
    )
    assert login.status_code == 200
    admin_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    stats = client.get("/admin/stats", headers=admin_headers)
    assert stats.status_code == 200
    body = stats.json()
    assert body["courses"] >= 5
    assert body["lessons"] >= 10
    assert body["learners"] >= 2


def test_assessment_flow():
    headers = register(email="assess@example.com")

    qs = client.get("/assessment/questions").json()
    assert len(qs) == 15
    cats = {q["category"] for q in qs}
    assert "Cloud" in cats and "Programming" in cats
    # answers must not leak
    assert "correct_answer" not in qs[0]

    # submit all-correct answers via DB (like quiz flow)
    from sqlalchemy import select

    from app.database import SessionLocal
    from app.models import AssessmentQuestion

    db = SessionLocal()
    try:
        rows = db.scalars(select(AssessmentQuestion)).all()
        answers = {str(q.id): q.correct_answer for q in rows}
    finally:
        db.close()

    res = client.post("/assessment/submit", headers=headers, json={"answers": answers}).json()
    assert res["saved"] is True
    assert res["overall_percent"] == 100
    assert len(res["scores"]) == 6
    assert res["recommended_pathway"] is not None
    assert res["reason"]

    profile = client.get("/me/profile", headers=headers).json()
    assert profile["assessment"] is not None
    assert profile["assessment"]["overall_percent"] == 100
    assert profile["assessment"]["recommended_pathway_id"] == res["recommended_pathway"]["id"]


def test_assessment_recommendation_default():
    headers = register(email="weak@example.com")
    qs = client.get("/assessment/questions").json()
    # all wrong
    answers = {str(q["id"]): "d" for q in qs}
    res = client.post("/assessment/submit", headers=headers, json={"answers": answers}).json()
    assert res["overall_percent"] < 50
    # defaults toward foundational IT Support pathway
    if res["recommended_pathway"]:
        assert res["recommended_pathway"]["title"] in (
            "IT Support Technician",
            "Digital Entrepreneur",
            "Junior Developer",
            "Cloud Practitioner",
            "Cybersecurity Analyst",
        )


def test_opportunities_public():
    r = client.get("/opportunities")
    assert r.status_code == 200
    opps = r.json()
    assert len(opps) >= 5
    types = {o["opportunity_type"] for o in opps}
    assert "Certification" in types
    # opportunity creation requires admin
    assert client.post("/opportunities", json={
        "title": "X", "organisation": "Y", "opportunity_type": "Job",
        "location": "Z", "closing_date": None, "description": "",
        "requirements": "", "url": None,
    }).status_code in (401, 403)


def test_certificate_issued_on_course_completion():
    headers = register(email="cert@example.com")

    # find a single-lesson course (AWS Cloud Fundamentals)
    courses = client.get("/courses").json()
    target = next(c for c in courses if c["title"] == "AWS Cloud Fundamentals")
    detail = client.get(f"/courses/{target['id']}").json()
    lesson_id = detail["modules"][0]["lessons"][0]["id"]

    client.post("/me/lessons/complete", headers=headers, json={"lesson_id": lesson_id})

    # no cert yet (quiz not passed)
    before = client.get("/me/certificates", headers=headers).json()
    assert all(c["course_id"] != target["id"] for c in before)

    # pass the quiz
    from sqlalchemy import select

    from app.database import SessionLocal
    from app.models import QuizQuestion

    db = SessionLocal()
    try:
        rows = db.scalars(select(QuizQuestion).where(QuizQuestion.lesson_id == lesson_id)).all()
        answers = {str(q.id): q.correct_answer for q in rows}
    finally:
        db.close()
    res = client.post(
        "/me/quizzes/submit", headers=headers, json={"lesson_id": lesson_id, "answers": answers}
    ).json()
    assert res["passed"] is True

    certs = client.get("/me/certificates", headers=headers).json()
    match = [c for c in certs if c["course_id"] == target["id"]]
    assert match, "certificate should be issued"
    assert match[0]["course_title"] == "AWS Cloud Fundamentals"


def test_next_lesson_personalised():
    headers = register(email="next@example.com")

    # no pathway ? first lesson overall
    nxt = client.get("/me/next-lesson", headers=headers).json()
    assert nxt["lesson_id"] >= 1

    # choose pathway ? next lesson follows pathway order
    client.post("/me/pathway", headers=headers, json={"pathway_id": 1})  # IT Support
    nxt2 = client.get("/me/next-lesson", headers=headers).json()
    assert nxt2["level_title"] is not None
    assert "LEVEL" in nxt2["level_title"]

    # complete that lesson ? moves forward
    client.post("/me/lessons/complete", headers=headers, json={"lesson_id": nxt2["lesson_id"]})
    nxt3 = client.get("/me/next-lesson", headers=headers).json()
    assert nxt3["lesson_id"] != nxt2["lesson_id"]
