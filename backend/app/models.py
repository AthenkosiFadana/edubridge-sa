from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(120), nullable=True)
    role: Mapped[str] = mapped_column(String(20), default="learner")  # learner | admin
    pathway_id: Mapped[int | None] = mapped_column(ForeignKey("pathways.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    progress: Mapped[list["Progress"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    quiz_results: Mapped[list["QuizResult"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    assessment_results: Mapped[list["AssessmentResult"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    pathway: Mapped["Pathway | None"] = relationship()


class Pathway(Base):
    """Career goal → ordered levels of courses."""

    __tablename__ = "pathways"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")
    role_title: Mapped[str] = mapped_column(String(120), default="")

    levels: Mapped[list["PathwayLevel"]] = relationship(
        back_populates="pathway", cascade="all, delete-orphan", order_by="PathwayLevel.order_number"
    )


class PathwayLevel(Base):
    __tablename__ = "pathway_levels"
    __table_args__ = (UniqueConstraint("pathway_id", "order_number"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pathway_id: Mapped[int] = mapped_column(ForeignKey("pathways.id"))
    order_number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(160))
    course_id: Mapped[int | None] = mapped_column(ForeignKey("courses.id"), nullable=True)

    pathway: Mapped["Pathway"] = relationship(back_populates="levels")
    course: Mapped["Course | None"] = relationship()


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(160), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str] = mapped_column(String(80), default="General")
    difficulty: Mapped[str] = mapped_column(String(20), default="Beginner")

    modules: Mapped[list["Module"]] = relationship(
        back_populates="course", cascade="all, delete-orphan", order_by="Module.order_number"
    )


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text, default="")
    order_number: Mapped[int] = mapped_column(Integer, default=1)

    course: Mapped["Course"] = relationship(back_populates="modules")
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order_number"
    )


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"))
    title: Mapped[str] = mapped_column(String(160))
    content: Mapped[str] = mapped_column(Text, default="")
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    resource_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    order_number: Mapped[int] = mapped_column(Integer, default=1)

    module: Mapped["Module"] = relationship(back_populates="lessons")
    quiz_questions: Mapped[list["QuizQuestion"]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan"
    )


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_id: Mapped[int | None] = mapped_column(ForeignKey("lessons.id"), nullable=True)
    module_id: Mapped[int | None] = mapped_column(ForeignKey("modules.id"), nullable=True)
    question: Mapped[str] = mapped_column(Text)
    option_a: Mapped[str] = mapped_column(String(300))
    option_b: Mapped[str] = mapped_column(String(300))
    option_c: Mapped[str] = mapped_column(String(300))
    option_d: Mapped[str] = mapped_column(String(300))
    correct_answer: Mapped[str] = mapped_column(String(1))  # a|b|c|d

    lesson: Mapped["Lesson | None"] = relationship(back_populates="quiz_questions")


class Progress(Base):
    __tablename__ = "progress"
    __table_args__ = (UniqueConstraint("user_id", "lesson_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    completed: Mapped[bool] = mapped_column(Boolean, default=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    user: Mapped["User"] = relationship(back_populates="progress")


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    lesson_id: Mapped[int | None] = mapped_column(ForeignKey("lessons.id"), nullable=True)
    module_id: Mapped[int | None] = mapped_column(ForeignKey("modules.id"), nullable=True)
    score: Mapped[int] = mapped_column(Integer)
    total: Mapped[int] = mapped_column(Integer)
    taken_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    user: Mapped["User"] = relationship(back_populates="quiz_results")


class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String(80))
    question: Mapped[str] = mapped_column(Text)
    option_a: Mapped[str] = mapped_column(String(300))
    option_b: Mapped[str] = mapped_column(String(300))
    option_c: Mapped[str] = mapped_column(String(300))
    option_d: Mapped[str] = mapped_column(String(300))
    correct_answer: Mapped[str] = mapped_column(String(1))


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    scores_json: Mapped[str] = mapped_column(Text, default="{}")
    recommended_pathway_id: Mapped[int | None] = mapped_column(ForeignKey("pathways.id"), nullable=True)
    taken_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    user: Mapped["User"] = relationship(back_populates="assessment_results")


class JobOpportunity(Base):
    __tablename__ = "job_opportunities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    organisation: Mapped[str] = mapped_column(String(160))
    opportunity_type: Mapped[str] = mapped_column(String(60))  # Learnership|YES|Internship|Job|Certification
    location: Mapped[str] = mapped_column(String(120), default="South Africa")
    closing_date: Mapped[str | None] = mapped_column(String(40), nullable=True)
    description: Mapped[str] = mapped_column(Text, default="")
    requirements: Mapped[str] = mapped_column(Text, default="")
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
