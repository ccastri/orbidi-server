from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import models
import crud
import schemas
import models
import db
from db import engine, Base
# from .db import engine, Base
from router.routes import recommendations_router
# from .router import locations, categories, recommendations
# from .router import locations, categories, recommendations

load_dotenv()

app = FastAPI(
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs"
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(locations.router, tags=["Locations"], prefix="/api")
# app.include_router(categories.router, tags=["Categories"], prefix="/api")
app.include_router(recommendations_router, tags=["Recommendations"], prefix="/api")
app.mount("/static", StaticFiles(directory="static"), name="static")

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()



if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
