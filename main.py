from os import name
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

from db import models
from db.database import engine
from db.hashing import Hash
from routers import client, signin
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# # Define OAuth2PasswordBearer instance
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# # Add security scheme to OpenAPI documentation
# app.openapi_schema["components"]["securitySchemes"] = {
#     "bearerAuth": {
#         "type": "http",
#         "scheme": "bearer",
#         "bearerFormat": "JWT",
#     }
# }

app.include_router(client.router)
app.include_router(signin.router)

@app.get("/")
def root():
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
    # Use this for debugging purposes only
    # logger.warning("Running in development mode. Do not run like this in production.")
    import uvicorn

    uvicorn.run(app, host="localhost", port=8801, log_level="debug")

# app.mount('/images', StaticFiles(directory='images'), name='images')