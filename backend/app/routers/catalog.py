from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..database import get_db
from ..models import Course, Module, Pathway
from ..schemas import CourseDetailOut, CourseOut, PathwayOut

router = APIRouter(tags=["catalog"])


@router.get("/courses", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.scalars(select(Course).order_by(Course.title)).all()


@router.get("/courses/{course_id}", response_model=CourseDetailOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.scalar(
        select(Course)
        .where(Course.id == course_id)
        .options(selectinload(Course.modules).selectinload(Module.lessons))
    )
    if course is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")
    return course


@router.get("/pathways", response_model=list[PathwayOut])
def list_pathways(db: Session = Depends(get_db)):
    return db.scalars(
        select(Pathway).options(selectinload(Pathway.levels)).order_by(Pathway.id)
    ).all()


@router.get("/pathways/{pathway_id}", response_model=PathwayOut)
def get_pathway(pathway_id: int, db: Session = Depends(get_db)):
    pathway = db.scalar(
        select(Pathway).where(Pathway.id == pathway_id).options(selectinload(Pathway.levels))
    )
    if pathway is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pathway not found")
    return pathway
