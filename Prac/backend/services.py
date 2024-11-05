from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from models import Category, Option, Vote, User
from schemas import Option

# Category Service

# create
def create_category(name: str, db: Session):
    query = text ("""
        INSERT INTO categories (name) VALUES (:name)
        """)
    db.execute(query,{"name": name})
    db.commit()
    return get_category_by_name(name, db)

# get
def get_categories(db: Session):
    query = text("""
        SELECT * FROM categories
        """)
    result = db.execute(query)
    return [{"category_id": row[0], "name": row[1]} for row in result]

def get_category_by_name(name: str, db: Session):
    query = text("""
        SELECT * FROM categories
        WHERE name = :name
        """)
    result = db.execute(query, {"name": name}).fetchone()
    return {"category_id": result[0], "name": result[1]} if result else None

# Option

# create
def create_option(name, category_id, db: Session):
    query = text("""
        INSERT INTO options (name, category_id) VALUES (:name, :category_id)
        """)
    db.execute(query, {"name": name, "category_id": category_id})
    db.commit()
    return get_option_by_name(name, db)


def get_option_by_name(name: str, db: Session):
    query = text("""
        SELECT * FROM options WHERE name = :name
        """)
    result = db.execute(query, {"name": name}).fetchone()
    return {"id": result[0], "name": result[1], "category_id": result[2]}

def get_options_by_category(id: int, db: Session) -> List[Option]:
    query = text("""
        SELECT * FROM options WHERE category_id = :id
        """)
    result = db.execute(query, {"id": id}).fetchall()  # Fetch all results
    
    # Build the response
    return [{"id": row[0], "name": row[1], "category_id": row[2]} for row in result]

# User
def create_user(id: int, db: Session):
    query = text("""
        INSERT INTO users (id) VALUES (:id)
        """)
    db.execute(query, {"id": id})
    db.commit()
    return get_user_by_id(id, db)

def get_user_by_id(id: int, db: Session):
    query = text("""
        SELECT * FROM users WHERE id = :id
        """)
    result = db.execute(query, {"id": id}).fetchone()
    return {"id": result[0]}

# Vote
def create_vote(id: int, category_id: int, option: int, db: Session):
    query = text("""
        INSERT INTO votes (user_id, category_id, option_id)
        VALUES(:id, :category_id, :option)
        ON DUPLICATE KEY UPDATE option_id = :option
        """)
    db.execute(query, {"id": id, "category_id": category_id, "option": option})
    db.commit()
    return {"user": id, "category": category_id, "option": option}

def refresh(db: Session):
    query = text("""
        SELECT c.id AS category_id, c.name AS category, o.id AS option_id, o.name AS option_name, COUNT(v.option_id) AS total_votes
        FROM categories c
        LEFT JOIN options o ON c.id = o.category_id
        LEFT JOIN votes v on o.category_id = v.category_id AND o.id = v.option_id
        GROUP BY c.name, o.name, c.id, o.id
        ORDER BY c.id, o.id 
        """)
    result = db.execute(query)
    return [
        {"category_id": row[0], "category_name": row[1], "option_id": row[2], "option": row[3], "total_votes": row[4]}
        for row in result
    ]

def rigging(db: Session):
    query = text("""
        SELECT c.id AS category_id, c.name AS category_name, o.id AS option_id,
        o.name AS option_name,
        CASE
            WHEN o.id = (
            SELECT MIN(o2.id) FROM options o2 WHERE o2.category_id = c.id
            )
            THEN (
            SELECT COUNT(*) FROM votes v2 WHERE v2.category_id = c.id
            )
            ELSE COUNT(v.option_id)
        END AS total_votes
        FROM categories c
        LEFT JOIN options o ON c.id = o.category_id
        LEFT JOIN votes v ON o.id = v.option_id AND o.category_id = v.category_id
        GROUP BY c.id, c.name, o.id, o.name
        ORDER BY c.id, o.id
        """)
    result = db.execute(query)
    db.commit()
    return [
        {"category_id": row[0], "category_name": row[1], "option_id": row[2], "option": row[3], "total_votes": row[4]}
        for row in result
    ] 