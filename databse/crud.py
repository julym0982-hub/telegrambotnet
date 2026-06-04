
from sqlalchemy.orm import Session
from .models import Message, Group

def get_message(db: Session):
    return db.query(Message).first()

def create_message(db: Session, text: str):
    db.query(Message).delete()
    db_message = Message(text=text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_groups(db: Session):
    return db.query(Group).all()

def get_group_by_link(db: Session, link: str):
    return db.query(Group).filter(Group.link == link).first()

def create_group(db: Session, link: str):
    db_group = Group(link=link)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_group(db: Session, link: str):
    db_group = db.query(Group).filter(Group.link == link).first()
    if db_group:
        db.delete(db_group)
        db.commit()
        return True
    return False

def delete_all_groups(db: Session):
    db.query(Group).delete()
    db.commit()
    return True
