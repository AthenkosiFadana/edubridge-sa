from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..database import get_db
from ..deps import get_current_user
from ..models import (
    Certificate,
    Course,
    Lesson,
    Module,
    Pathway,
    Progress,
    QuizQuestion,
    QuizResult,
    User,
)
from ..schemas import (
    CertificateOut,
    CategorySkill,
    CompleteLessonIn,
    LatestAssessment,
    LessonDetailOut,
    NextLessonOut,
    ProgressOut,
    QuizResultOut,
    SkillsProfileOut,
    SubmitQuizIn,
)
from ..services import latest_assessment, next_lesson_for_user, parse_scores, try_issue_certificates

router = APIRouter(prefix="/me", tags=["me"])


@router.post("/pathway", status_code=status.HTTP_200_OK)
def choose_pathway(
    data: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pathway = db.get(Pathway, data.get("pathway_id", 0))
    if pathway is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pathway not found")
    user.pathway_id = pathway.id
    db.commit()
    return {"pathway_id": pathway.id, "title": pathway.title}


@router.get("/lessons/{lesson_id}/content", response_model=LessonDetailOut)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Lesson not found")
    return lesson


@router.post("/lessons/complete", response_model=ProgressOut, status_code=status.HTTP_201_CREATED)
def complete_lesson(
    data: CompleteLessonIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson = db.get(Lesson, data.lesson_id)
    if lesson is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Lesson not found")
    existing = db.scalar(
        select(Progress).where(Progress.user_id == user.id, Progress.lesson_id == lesson.id)
    )
    if existing is None:
        progress = Progress(user_id=user.id, lesson_id=lesson.id, completed=True)
        db.add(progress)
        db.commit()
        db.refresh(progress)
        try_issue_certificates(db, user)
        return progress
    try_issue_certificates(db, user)
    return existing


@router.post("/quizzes/submit", response_model=QuizResultOut)
def submit_quiz(
    data: SubmitQuizIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    questions = db.scalars(
        select(QuizQuestion).where(QuizQuestion.lesson_id == data.lesson_id)
    ).all()
    if not questions:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No quiz for this lesson")

    correct = 0
    incorrect: list[dict] = []
    for q in questions:
        given = (data.answers.get(str(q.id)) or data.answers.get(q.id) or "").lower()
        if given == q.correct_answer:
            correct += 1
        else:
            incorrect.append({"question_id": q.id, "question": q.question, "correct": q.correct_answer})

    total = len(questions)
    result = QuizResult(user_id=user.id, lesson_id=data.lesson_id, score=correct, total=total)
    db.add(result)
    db.commit()
    try_issue_certificates(db, user)

    percent = round(correct / total * 100)
    return QuizResultOut(
        score=correct, total=total, percent=percent, passed=percent >= 70, incorrect=incorrect
    )


@router.get("/progress", response_model=list[ProgressOut])
def my_progress(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.scalars(select(Progress).where(Progress.user_id == user.id)).all()


@router.get("/next-lesson", response_model=NextLessonOut)
def my_next_lesson(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    nxt = next_lesson_for_user(db, user)
    if nxt is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "All lessons completed")
    return nxt


@router.get("/profile", response_model=SkillsProfileOut)
def skills_profile(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try_issue_certificates(db, user)

    done_ids = set(
        db.scalars(select(Progress.lesson_id).where(Progress.user_id == user.id)).all()
    )
    lessons = db.scalars(select(Lesson)).all()
    lessons_total = len(lessons)
    lessons_completed = sum(1 for l in lessons if l.id in done_ids)

    passed_quizzes = db.scalars(select(QuizResult).where(QuizResult.user_id == user.id)).all()
    quizzes_passed = sum(1 for r in passed_quizzes if r.total and r.score / r.total >= 0.7)

    # Category skills: % of lessons completed per course category
    cat_stats: dict[str, dict[str, int]] = {}
    courses = db.scalars(
        select(Course).options(selectinload(Course.modules).selectinload(Module.lessons))
    ).all()
    badges: list[str] = []
    for course in courses:
        cat = cat_stats.setdefault(course.category, {"done": 0, "total": 0})
        course_lessons = [l for m in course.modules for l in m.lessons]
        cat["total"] += len(course_lessons)
        cat["done"] += sum(1 for l in course_lessons if l.id in done_ids)
        if course_lessons and all(l.id in done_ids for l in course_lessons):
            badges.append(course.title)

    category_skills = [
        CategorySkill(
            category=cat,
            percent=round(v["done"] / v["total"] * 100, 1) if v["total"] else 0.0,
        )
        for cat, v in sorted(cat_stats.items())
    ]

    pathway = db.get(Pathway, user.pathway_id) if user.pathway_id else None

    certs = db.scalars(
        select(Certificate).where(Certificate.user_id == user.id)
    ).all()
    cert_out: list[CertificateOut] = []
    for c in certs:
        course = db.get(Course, c.course_id)
        cert_out.append(
            CertificateOut(
                id=c.id,
                course_id=c.course_id,
                course_title=course.title if course else f"Course {c.course_id}",
                issued_at=c.issued_at,
            )
        )

    assessment_row = latest_assessment(db, user)
    assessment = None
    if assessment_row:
        assessment = LatestAssessment(
            taken_at=assessment_row.taken_at,
            overall_percent=round(
                sum(s["score"] for s in parse_scores(assessment_row))
                / max(sum(s["total"] for s in parse_scores(assessment_row)), 1)
                * 100
            ),
            scores=parse_scores(assessment_row),
            recommended_pathway_id=assessment_row.recommended_pathway_id,
        )

    next_lesson = next_lesson_for_user(db, user)
    percent = round(lessons_completed / lessons_total * 100, 1) if lessons_total else 0.0

    return SkillsProfileOut(
        lessons_completed=lessons_completed,
        lessons_total=lessons_total,
        percent=percent,
        quizzes_passed=quizzes_passed,
        badges=badges,
        pathway=pathway,
        certificates=cert_out,
        category_skills=category_skills,
        next_lesson=NextLessonOut(**next_lesson) if next_lesson else None,
        assessment=assessment,
    )


@router.get("/certificates", response_model=list[CertificateOut])
def my_certificates(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try_issue_certificates(db, user)
    rows = db.scalars(select(Certificate).where(Certificate.user_id == user.id)).all()
    out = []
    for c in rows:
        course = db.get(Course, c.course_id)
        out.append(
            CertificateOut(
                id=c.id,
                course_id=c.course_id,
                course_title=course.title if course else f"Course {c.course_id}",
                issued_at=c.issued_at,
            )
        )
    return out
