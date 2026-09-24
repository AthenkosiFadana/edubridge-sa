from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import require_admin
from ..models import Certificate, Course, Lesson, QuizResult, User
from ..schemas import AdminStatsOut, UserOut

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStatsOut)
def stats(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    learners = db.scalar(select(func.count(User.id))) or 0
    courses = db.scalar(select(func.count(Course.id))) or 0
    lessons = db.scalar(select(func.count(Lesson.id))) or 0
    quiz_results = db.scalar(select(func.count(QuizResult.id))) or 0
    certificates = db.scalar(select(func.count(Certificate.id))) or 0

    distinct_learners_done = db.scalar(select(func.count(func.distinct(QuizResult.user_id)))) or 0
    completion_rate = round(distinct_learners_done / learners * 100, 1) if learners else 0.0

    return AdminStatsOut(
        learners=learners,
        courses=courses,
        lessons=lessons,
        quiz_results=quiz_results,
        certificates=certificates,
        completion_rate=completion_rate,
    )


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.scalars(select(User).order_by(User.created_at.desc())).all()
