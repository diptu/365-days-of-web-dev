# app.schemas.student
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class StudentSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    course_of_study: str = Field(...)
    year: int = Field(..., gt=0, lt=9)
    gpa: float = Field(..., le=4.0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "fullname": "Nazmul Alam",
                    "email": "diptunazmulalam@gmail.com",
                    "course_of_study": "Computer Science and engineering",
                    "year": 2,
                    "gpa": "3.0",
                }
            ]
        }
    }


class UpdateStudentSchema(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    course_of_study: Optional[str]
    year: Optional[int]
    gpa: Optional[float]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "fullname": "Nazmul Alam",
                    "email": "nazmul.diptu@northsouth.edu",
                    "course_of_study": "Computer Science and engineering",
                    "year": 4,
                    "gpa": "3.62",
                }
            ]
        }
    }
