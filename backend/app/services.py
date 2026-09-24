"""Shared domain logic: certificate issuance and next-lesson personalisation."""

import json

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from .models import (
    AssessmentResult,
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


def course_lesson_ids(course: Course) -> set[int]:
    return {l.id for m in course.modules for l in m.lessons}


def course_quiz_lesson_ids(course: Course) -> set[int]:
    ids = set()
    for m in course.modules:
        for l in m.lessons:
            if l.quiz_questions:
                ids.add(l.id)
    return ids


def try_issue_certificates(db: Session, user: User) -> list[Certificate]:
    """Issue certificates for any course the user has fully completed.

    Criteria: every lesson completed AND every lesson with a quiz has a
    passed attempt (>= 70%).
    """
    completed = set(
        db.scalars(select(Progress.lesson_id).where(Progress.user_id == user.id)).all()
    )
    passed_lessons = set(
        db.scalars(
            select(QuizResult.lesson_id).where(
                QuizResult.user_id == user.id,
                QuizResult.lesson_id.is_not(None),
            )
        ).all()
    )
    # a lesson counts as passed if any attempt reached 70%
    best: dict[int, float] = {}
    for r in db.scalars(select(QuizResult).where(QuizResult.user_id == user.id)).all():
        if r.lesson_id is None or r.total == 0:
            continue
        pct = r.score / r.total
        best[r.lesson_id] = max(best.get(r.lesson_id, 0.0), pct)
    passed_lessons = {lid for lid, pct in best.items() if pct >= 0.7}

    existing = {
        c.course_id
        for c in db.scalars(select(Certificate).where(Certificate.user_id == user.id)).all()
    }

    issued: list[Certificate] = []
    courses = db.scalars(
        select(Course).options(
            selectinload(Course.modules).selectinload(Module.lessons).selectinload(Lesson.quiz_questions)
        )
    ).all()
    for course in courses:
        if course.id in existing:
            continue
        lessons = course_lesson_ids(course)
        if not lessons or not lessons <= completed:
            continue
        quiz_lessons = course_quiz_lesson_ids(course)
        if not quiz_lessons <= passed_lessons:
            continue
        cert = Certificate(user_id=user.id, course_id=course.id)
        db.add(cert)
        issued.append(cert)
    if issued:
        db.commit()
        for c in issued:
            db.refresh(c)
    return issued


def next_lesson_for_user(db: Session, user: User) -> dict | None:
    """First incomplete lesson along the user's chosen pathway (or all courses)."""
    completed = set(
        db.scalars(select(Progress.lesson_id).where(Progress.user_id == user.id)).all()
    )

    courses: list[Course] = []
    level_titles: dict[int, str] = {}
    if user.pathway_id:
        pathway = db.scalar(
            select(Pathway)
            .where(Pathway.id == user.pathway_id)
            .options(selectinload(Pathway.levels))
        )
        for lvl in pathway.levels:
            if lvl.course_id:
                course = db.scalar(
                    select(Course)
                    .where(Course.id == lvl.course_id)
                    .options(
                        selectinload(Course.modules).selectinload(Module.lessons).selectinload(Lesson.quiz_questions)
                    )
                )
                if course:
                    courses.append(course)
                    level_titles[course.id] = lvl.title

    if not courses:
        courses = db.scalars(
            select(Course).options(
                selectinload(Course.modules).selectinload(Module.lessons).selectinload(Lesson.quiz_questions)
            )
        ).all()

    for course in courses:
        for module in sorted(course.modules, key=lambda m: m.order_number):
            for lesson in sorted(module.lessons, key=lambda l: l.order_number):
                if lesson.id not in completed:
                    return {
                        "lesson_id": lesson.id,
                        "title": lesson.title,
                        "course_id": course.id,
                        "course_title": course.title,
                        "module_title": module.title,
                        "level_title": level_titles.get(course.id),
                    }
    return None


def latest_assessment(db: Session, user: User) -> AssessmentResult | None:
    return db.scalar(
        select(AssessmentResult)
        .where(AssessmentResult.user_id == user.id)
        .order_by(AssessmentResult.taken_at.desc())
        .limit(1)
    )


def parse_scores(result: AssessmentResult) -> list[dict]:
    try:
        data = json.loads(result.scores_json)
    except json.JSONDecodeError:
        return []
    return [
        {"category": k, "score": v["score"], "total": v["total"], "percent": v["percent"]}
        for k, v in data.items()
    ]
