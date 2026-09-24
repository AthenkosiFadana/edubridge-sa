from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import require_admin
from ..models import JobOpportunity, User
from ..schemas import OpportunityOut

router = APIRouter(tags=["opportunities"])


@router.get("/opportunities", response_model=list[OpportunityOut])
def list_opportunities(db: Session = Depends(get_db)):
    return db.scalars(select(JobOpportunity).order_by(JobOpportunity.id)).all()


@router.get("/opportunities/{opp_id}", response_model=OpportunityOut)
def get_opportunity(opp_id: int, db: Session = Depends(get_db)):
    opp = db.get(JobOpportunity, opp_id)
    if opp is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Opportunity not found")
    return opp


@router.post("/opportunities", response_model=OpportunityOut, status_code=status.HTTP_201_CREATED)
def create_opportunity(data: OpportunityOut, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    opp = JobOpportunity(**data.model_dump())
    db.add(opp)
    db.commit()
    db.refresh(opp)
    return opp
