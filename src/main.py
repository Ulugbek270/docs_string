from fastapi import FastAPI
import logging
from src.routers import auth, extract
from src.db.base import Base,engine


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(engine)
app = FastAPI()


@app.get("/")
async def healthy_check():
    return {"health": "good"}


app.include_router(auth.app)
app.include_router(extract.app)

# if __name__ == "__main__":
   
#     uvicorn.run(app, host="0.0.0.0", port=8011, reload=True)