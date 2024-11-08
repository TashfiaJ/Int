from fastapi import FastAPI
from controllers import router
from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind = engine)

app.include_router(router)
