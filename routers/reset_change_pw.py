#reset_change_pw.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import client_db
from schemas.client import ResetPassword
from db.database import get_db

router = APIRouter(
    prefix='/pw',
    tags=['password']
)

@router.post("/reset/me/", response_model=ResetPassword)
async def request_password_reset(email: str, db: Session = Depends(get_db)):
    client = client_db.get_client_by_email(db, email)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found",
        )

    # Assume you generate a token for password reset (this is a simplified example)
    reset_token = client_db.create_password_reset_token(db, email)

    # In a real application, you would send an email to the user with a link containing the reset_token
    # Here you can use a library like SendGrid, SMTP, or any other email service

    return {"message": f"Password reset initiated. Check your email for instructions."}


@router.get("/change/me/", response_model=ResetPassword)
def change_password():
    return True