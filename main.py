from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers.employee_router import router as employee_router
from routers import employee_personal_router

app = FastAPI()

app.include_router(employee_router)
app.include_router(employee_personal_router.router)
