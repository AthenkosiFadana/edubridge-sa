from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# Auth
class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    location: str | None = None


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    location: str | None
    role: str
    pathway_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class ChoosePathwayIn(BaseModel):
    pathway_id: int


# Catalog
class QuizQuestionOut(BaseModel):
    id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        from_attributes = True


class LessonOut(BaseModel):
    id: int
    title: str
    content: str
    video_url: str | None
    resource_url: str | None
    order_number: int

    class Config:
        from_attributes = True


class LessonDetailOut(LessonOut):
    quiz_questions: list[QuizQuestionOut] = []


class ModuleOut(BaseModel):
    id: int
    title: str
    description: str
    order_number: int

    class Config:
        from_attributes = True


class ModuleDetailOut(ModuleOut):
    lessons: list[LessonOut] = []


class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    category: str
    difficulty: str

    class Config:
        from_attributes = True


class CourseDetailOut(CourseOut):
    modules: list[ModuleDetailOut] = []


class PathwayLevelOut(BaseModel):
    id: int
    order_number: int
    title: str
    course_id: int | None
    course: CourseOut | None = None

    class Config:
        from_attributes = True


class PathwayOut(BaseModel):
    id: int
    title: str
    description: str
    role_title: str
    levels: list[PathwayLevelOut] = []

    class Config:
        from_attributes = True


# Progress & quizzes
class CompleteLessonIn(BaseModel):
    lesson_id: int


class SubmitQuizIn(BaseModel):
    lesson_id: int
    answers: dict[int, str]  # question_id -> a|b|c|d


class QuizResultOut(BaseModel):
    score: int
    total: int
    percent: int
    passed: bool
    incorrect: list[dict]


class ProgressOut(BaseModel):
    lesson_id: int
    completed: bool
    completed_at: datetime

    class Config:
        from_attributes = True


class SkillsProfileOut(BaseModel):
    lessons_completed: int
    lessons_total: int
    percent: float
    quizzes_passed: int
    badges: list[str]
    pathway: PathwayOut | None
    certificates: list["CertificateOut"] = []
    category_skills: list["CategorySkill"] = []
    next_lesson: "NextLessonOut | None" = None
    assessment: "LatestAssessment | None" = None


# Admin
class AdminStatsOut(BaseModel):
    learners: int
    courses: int
    lessons: int
    quiz_results: int
    certificates: int
    completion_rate: float


# Phase 3
class AssessmentQuestionOut(BaseModel):
    id: int
    category: str
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        from_attributes = True


class AssessmentSubmitIn(BaseModel):
    answers: dict[int, str]


class CategoryScore(BaseModel):
    category: str
    score: int
    total: int
    percent: int


class AssessmentResultOut(BaseModel):
    scores: list[CategoryScore]
    overall_percent: int
    recommended_pathway: PathwayOut | None
    reason: str
    saved: bool


class OpportunityOut(BaseModel):
    id: int
    title: str
    organisation: str
    opportunity_type: str
    location: str
    closing_date: str | None
    description: str
    requirements: str
    url: str | None

    class Config:
        from_attributes = True


class CertificateOut(BaseModel):
    id: int
    course_id: int
    course_title: str
    issued_at: datetime


class NextLessonOut(BaseModel):
    lesson_id: int
    title: str
    course_id: int
    course_title: str
    module_title: str
    level_title: str | None = None


class CategorySkill(BaseModel):
    category: str
    percent: float


class LatestAssessment(BaseModel):
    taken_at: datetime
    overall_percent: int
    scores: list[CategoryScore]
    recommended_pathway_id: int | None
