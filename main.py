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
from router.locations import location_router
from router.categories import category_router
from router.routes import recommendations_router
import os
# from .db import engine, Base
# from .router import locations, categories, recommendations
# from .router import locations, categories, recommendations

load_dotenv()

app = FastAPI(
 servers=[
        {"url": "http://localhost:8002", "description": "Staging environment"},
        {"url": "http://localhost:8001", "description": "Production environment"},
    ],
    root_path="/api/v1",
    # root_path_in_servers=False
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Determinar la URL del servidor basado en la variable de entorno
environment = os.getenv("ENVIRONMENT", "development")
if environment == "production":
    server_url = "http://localhost:8001"
elif environment == "test":
    server_url = "http://localhost:8002"
else:
    server_url = "http://localhost:8000"  # Entorno de desarrollo por defecto

app.servers = [
    {"url": server_url, "description": f"{environment.capitalize()} environment"}
]


app.include_router(location_router, tags=["Locations"])
app.include_router(category_router, tags=["Categories"])
app.include_router(recommendations_router, tags=["Recommendations"])
app.mount("/static", StaticFiles(directory="static"), name="static")

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()



if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True, host="127.0.0.1",  port=8000)
