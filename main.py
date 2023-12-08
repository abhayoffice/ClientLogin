# main.py
from os import name

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from logger import logging
from db import models
from fastapi_mail import FastMail, ConnectionConfig
from db.database import engine
from db.hashing import Hash
from routers import client, signin, reset_change_pw
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=True)

load_dotenv()

# Email configuration
# conf = ConnectionConfig(
#     # MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
#     MAIL_USERNAME="abhay",
#     # MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
#     MAIL_PASSWORD="Netsmartz@1386",
#     # MAIL_FROM=os.getenv("MAIL_ID"),
#     MAIL_FROM="netsmartzeknoor@gmail.com",
#     MAIL_PORT=587,
#     MAIL_SERVER="mail server",
#     MAIL_FROM_NAME="Desired Name",
#     MAIL_STARTTLS=True,
#     MAIL_SSL_TLS=False,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True
# )

print("Working of fastMail initialized")

# mail = FastMail(conf)

#Include the routers
app.include_router(client.router)
app.include_router(signin.router)
app.include_router(reset_change_pw.router)

@app.get("/")
def root():
    logging.info("Received a request at the root endpoint.")
    return "Hello world!"

origins = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3002'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

models.Base.metadata.create_all(engine)

if __name__ == "__main__":
    logging.info("Starting the application.")
    # Use this for debugging purposes only
    # logger.warning("Running in development mode. Do not run like this in production.")
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8801, log_level="debug", reload=True)

# app.mount('/images', StaticFiles(directory='images'), name='images')
