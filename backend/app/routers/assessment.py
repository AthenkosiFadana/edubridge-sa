import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import AssessmentQuestion, AssessmentResult, Pathway, User
from ..schemas import AssessmentQuestionOut, AssessmentResultOut, AssessmentSubmitIn, CategoryScore
from ..services import try_issue_certificates

router = APIRouter(prefix="/assessment", tags=["assessment"])

# Map strongest categories to a recommended career pathway
RECOMMENDATION_RULES = [
    # (primary categories, pathway title, reason)
    ({"Programming"}, "Junior Developer", "Your programming score is your strongest area — a development pathway fits."),
    ({"Cloud"}, "Cloud Practitioner", "Cloud concepts came naturally to you — aim for AWS Cloud fundamentals next."),
    ({"Networking", "Security"}, "Cybersecurity Analyst", "Strong networking/security instincts point toward security work."),
    ({"Office Productivity", "Internet Skills"}, "Digital Entrepreneur", "You're strong with productivity and internet tools — ideal for running a digital business."),
]


@router.get("/questions", response_model=list[AssessmentQuestionOut])
def get_questions(db: Session = Depends(get_db)):
    questions = db.scalars(select(AssessmentQuestion).order_by(AssessmentQuestion.id)).all()
    if not questions:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Assessment not available yet")
    return questions


@router.post("/submit", response_model=AssessmentResultOut)
def submit_assessment(
    data: AssessmentSubmitIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    questions = db.scalars(select(AssessmentQuestion).order_by(AssessmentQuestion.id)).all()
    if not questions:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Assessment not available yet")

    by_cat: dict[str, dict[str, int]] = {}
    for q in questions:
        cat = by_cat.setdefault(q.category, {"score": 0, "total": 0})
        cat["total"] += 1
        given = (data.answers.get(str(q.id)) or data.answers.get(q.id) or "").lower()
        if given == q.correct_answer:
            cat["score"] += 1

    scores = []
    stored: dict[str, dict[str, int]] = {}
    total_score = total_q = 0
    for cat, v in by_cat.items():
        percent = round(v["score"] / v["total"] * 100)
        scores.append(CategoryScore(category=cat, score=v["score"], total=v["total"], percent=percent))
        stored[cat] = {"score": v["score"], "total": v["total"], "percent": percent}
        total_score += v["score"]
        total_q += v["total"]

    overall = round(total_score / total_q * 100) if total_q else 0

    # Recommendation: highest-scoring rule match, else default
    recommended: Pathway | None = None
    reason = ""
    cat_percents = {s.category: s.percent for s in scores}
    for cats, title, why in RECOMMENDATION_RULES:
        if cats & set(cat_percents):
            best = max((cat_percents[c] for c in cats if c in cat_percents), default=0)
            if best >= 50:
                recommended = db.scalar(select(Pathway).where(Pathway.title == title))
                if recommended:
                    reason = why
                    break

    if recommended is None:
        # default: everything below 50% → foundations → IT Support
        recommended = db.scalar(select(Pathway).where(Pathway.title == "IT Support Technician"))
        reason = (
            "You're at the start of your journey — the IT Support pathway builds every "
            "foundation step by step, from computer basics onward."
        )

    result = AssessmentResult(
        user_id=user.id,
        scores_json=json.dumps(stored),
        recommended_pathway_id=recommended.id if recommended else None,
    )
    db.add(result)
    db.commit()

    return AssessmentResultOut(
        scores=scores,
        overall_percent=overall,
        recommended_pathway=recommended,
        reason=reason,
        saved=True,
    )
