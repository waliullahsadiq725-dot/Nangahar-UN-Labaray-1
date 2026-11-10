from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.api.deps import DbSession, require_roles
from app.models.user import User, UserRole, AccountStatus
from app.schemas.auth import UserOut

router = APIRouter(prefix="/admin", tags=["Administration"])
AdminOnly = Annotated[User, Depends(require_roles(UserRole.admin))]

@router.get("/pending-users", response_model=list[UserOut])
def pending_users(db: DbSession, _: AdminOnly):
    return list(db.scalars(select(User).where(User.status == AccountStatus.pending).order_by(User.created_at)))

@router.patch("/users/{user_id}/activate", response_model=UserOut)
def activate_user(user_id: int, db: DbSession, _: AdminOnly):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "کاروونکی ونه موندل شو")
    user.status = AccountStatus.active
    db.commit()
    db.refresh(user)
    return user

@router.patch("/users/{user_id}/suspend", response_model=UserOut)
def suspend_user(user_id: int, db: DbSession, _: AdminOnly):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "کاروونکی ونه موندل شو")
    user.status = AccountStatus.suspended
    db.commit()
    db.refresh(user)
    return user
