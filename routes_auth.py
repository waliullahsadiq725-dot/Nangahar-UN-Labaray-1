from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from typing import Annotated
from app.api.deps import DbSession, get_current_user
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User, UserRole, AccountStatus
from app.schemas.auth import RegisterIn, LoginIn, TokenOut, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: RegisterIn, db: DbSession):
    if data.role == UserRole.admin:
        raise HTTPException(403, "د Admin حساب یوازې د سرور له خوندي پروسې جوړېږي")
    if data.role == UserRole.student and data.staff_number:
        raise HTTPException(400, "محصل د استاد د پېژندشمېرې کارولای نه شي")
    if data.role == UserRole.teacher and data.student_number:
        raise HTTPException(400, "استاد د محصلۍ شمېرې کارولای نه شي")
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(409, "دا ایمیل مخکې ثبت شوی دی")
    if data.role == UserRole.student and not data.student_number:
        raise HTTPException(400, "د محصلۍ شمېره اړینه ده")
    if data.role == UserRole.teacher and not data.staff_number:
        raise HTTPException(400, "د استاد د کارکوونکي شمېره اړینه ده")
    user = User(full_name=data.full_name, email=data.email, password_hash=hash_password(data.password),
                role=data.role, status=AccountStatus.pending, faculty_id=data.faculty_id,
                department_id=data.department_id, student_number=data.student_number,
                staff_number=data.staff_number)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: DbSession):
    user = db.scalar(select(User).where(User.email == data.email))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "ایمیل یا پاسورډ ناسم دی")
    if user.status != AccountStatus.active:
        raise HTTPException(403, "اکوانټ مو لا د اډمین له خوا نه دی فعال شوی")
    return {"access_token": create_access_token(str(user.id)), "user": user}

@router.get("/me", response_model=UserOut)
def me(user: Annotated[User, Depends(get_current_user)]):
    return user
