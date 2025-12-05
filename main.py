from fastapi import APIRouter, FastAPI
from Router.user import user_router
from Router.post import post_router
from Router.auth_router import auth_router

app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mini Social Media Feed API"}