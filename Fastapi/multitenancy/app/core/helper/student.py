from typing import Iterable, Optional
from sqlalchemy.orm import Session
from app.core.models import Student
from app.core.schemas.student import StudentCreate, StudentUpdate


def create_student(db: Session, data: StudentCreate) -> Student:
    obj = Student(full_name=data.full_name, email=data.email)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_student(
    db: Session, student_id: int, data: StudentUpdate
) -> Optional[Student]:
    obj = db.get(Student, student_id)
    if not obj:
        return None
    if data.full_name is not None:
        obj.full_name = data.full_name
    if data.email is not None:
        obj.email = data.email
    db.commit()
    db.refresh(obj)
    return obj


def get_student(db: Session, student_id: int) -> Optional[Student]:
    return db.get(Student, student_id)


def list_students(db: Session) -> Iterable[Student]:
    return db.query(Student).order_by(Student.id.asc()).all()


def delete_student(db: Session, student_id: int) -> bool:
    obj = db.get(Student, student_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
