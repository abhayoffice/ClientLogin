# reset_change_pw.py
import os
from typing import Any, Dict

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import client_db
from db.models import DbClient
from schemas.client import ResetPassword
from db.database import get_db
from logger import logging

router = APIRouter(
    prefix='/api/v1/auth/pw',
    tags=['password']
)

load_dotenv()

conf = ConnectionConfig(
    # MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_USERNAME="abhay",
    # MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_PASSWORD="Netsmartz@1386",
    # MAIL_FROM=os.getenv("MAIL_ID"),
    MAIL_FROM="netsmartzeknoor@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="mail server",
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

mail = FastMail(conf)


@router.post("/reset/me/")
async def request_password_reset(email: str, db: Session = Depends(get_db)):
    logging.info(f"Received a request to initiate password reset for email: {email}")

    client = client_db.get_client_by_email(db, email)
    if not client:
        logging.warning(f"User with email {email} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found",
        )

    # Assume you generate a token for password reset (this is a simplified example)
    # reset_token = client_db.create_password_reset_token(db, email)

    # In a real application, you would send an email to the user with a link containing the reset_token
    subject = "Password Reset Request"
    # body = f"Click the following link to reset your password: http://example.com/reset?token={reset_token}"
    body = f"Click the following link to reset your password: http://localhost:8801/docs#/reset/confirm"

    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="html"
    )

    await mail.send_message(message)
    logging.info(f"Password reset initiated. Check your email for instructions.")

    return {"message": "Password reset initiated. Check your email for instructions."}

@router.post("/reset/confirm/")
async def confirm_password_reset(reset_data: ResetPassword, db: Session = Depends(get_db)) -> dict or None:
    logging.info("Received a request to confirm password reset.")

    reset_code = reset_data.reset_code
    new_password = reset_data.new_pass

    response = client_db.update_password_by_reset_code(db, reset_code, new_password)
    # response = client_db.update_password_by_reset_code(db, new_password)

    return response

# @router.get("/change/me/", response_model=ResetPassword)
# def change_password() :
#     logging.info("Received a request to change the password.")
#     return {"True":"Always True"}
