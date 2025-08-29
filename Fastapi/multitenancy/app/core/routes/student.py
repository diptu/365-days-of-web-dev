from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db.database import get_db, get_tenant
from app.core.schemas.student import StudentOut, StudentCreate, StudentUpdate
from app.core.helper import student as crud
from app.core.helper.response import success_response, error_response

router = APIRouter(tags=["students"])


@router.post("/", status_code=201)
def create_student(
    payload: StudentCreate,
    tenant_schema: str = Depends(get_tenant),
    db: Session = Depends(get_db),
):
    student = crud.create_student(db, payload)
    return success_response(
        message="Student created successfully",
        details=StudentOut.model_validate(student).dict(),
        code="STUDENT_CREATED",
        status_code=201,
    )


@router.get("/{student_id}")
def read_student(
    student_id: int,
    tenant_schema: str = Depends(get_tenant),
    db: Session = Depends(get_db),
):
    student = crud.get_student(db, student_id)
    if not student:
        return error_response(
            message="Student not found",
            details={"student_id": student_id},
            code="STUDENT_NOT_FOUND",
            status_code=404,
        )
    return success_response(
        message="Student retrieved successfully",
        details=StudentOut.model_validate(student).dict(),
        code="STUDENT_FOUND",
    )
