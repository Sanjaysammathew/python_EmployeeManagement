from fastapi import FastAPI
from routers.employee_router import router

app = FastAPI()

app.include_router(router)