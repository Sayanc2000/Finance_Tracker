from fastapi import FastAPI

from app.routers import auth, entries, user
from app.schemas import DefaultResponse, ErrorResponse

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(entries.router)


@app.get("/", response_model=DefaultResponse)
def root():
    return {"message": "Hello World"}


@app.get("/health", response_model=DefaultResponse)
def health():
    return {"message": "OK"}
