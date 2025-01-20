from sqlalchemy.orm import Session
from models import Shortcut


def create_shortcut(db: Session, command: str, result: str):
    full_command = command + " "
    db_shortcut = Shortcut(command=full_command, result=result)
    db.add(db_shortcut)
    db.commit()
    db.refresh(db_shortcut)
    return db_shortcut


def get_shortcut(db: Session, command: str):
    return db.query(Shortcut).filter(command == Shortcut.command).first()


def get_shortcuts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Shortcut).offset(skip).limit(limit).all()


def update_shortcut(db: Session, command: str, result: str):
    full_command = command + " "
    db_shortcut = get_shortcut(db, full_command)
    if db_shortcut:
        db_shortcut.command = full_command
        db_shortcut.result = result
        db.commit()
        db.refresh(db_shortcut)
    return db_shortcut


def delete_shortcut(db: Session, command: str):
    full_command = command + " "
    db_shortcut = get_shortcut(db, full_command)
    if db_shortcut:
        db.delete(db_shortcut)
        db.commit()
    return db_shortcut
