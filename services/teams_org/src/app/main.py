import uvicorn
from fastapi import FastAPI

from app.api.companies import cmp_router
from app.api.invites import inv_router
from app.api.teams import teams_router

app = FastAPI()

app.include_router(cmp_router, prefix="/companies")
app.include_router(teams_router)
app.include_router(inv_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8081, reload=True)
