import uvicorn
from fastapi import FastAPI
from app.api.companies import cmp_router


app = FastAPI()

app.include_router(cmp_router, prefix="/companies")

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8081, reload=True)
