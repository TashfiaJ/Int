from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import Category, Option, User
from services import (
    create_category, get_categories, create_option, get_options_by_category,
    create_user, create_vote, refresh, rigging
)


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Category
@router.post("/categories", response_model = Category)
def add_category(name: str, db: Session = Depends(get_db)):
    return create_category(name, db)

@router.get("/categories", response_model = list[Category])
def read_categories(db: Session = Depends(get_db)):
    return get_categories(db)

# Option
@router.post("/options", response_model = Option)
def add_option(name: str, category_id: int, db: Session = Depends(get_db)):
    return create_option(name, category_id, db)

@router.get("/options/{id}", response_model = list[Option])
def read_options(id: int, db: Session = Depends(get_db)):
    return get_options_by_category(id, db)

# User
@router.post("/user", response_model = User)
def add_user(id: int, db: Session = Depends(get_db)):
    return create_user(id, db)

#Vote
@router.post("/vote")
def add_vote(id: int, category: int, option: int, db: Session = Depends(get_db)):
    return create_vote(id, category, option, db)

@router.get("/refresh")
def refreshing(db: Session = Depends(get_db)):
    return refresh(db)

@router.get("/rigging")
def get_rigged_votes(db: Session = Depends(get_db)):
    return rigging(db)