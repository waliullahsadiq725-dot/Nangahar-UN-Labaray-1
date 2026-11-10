from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.user import UserRole, AccountStatus

class RegisterIn(BaseModel):
    full_name: str = Field(min_length=3, max_length=160)
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)
    role: UserRole
    faculty_id: int | None = None
    department_id: int | None = None
    student_number: str | None = Field(default=None, max_length=50)
    staff_number: str | None = Field(default=None, max_length=50)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    status: AccountStatus
    faculty_id: int | None
    department_id: int | None

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
