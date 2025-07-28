from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import auth
import app.models
from app.database import Base, engine
from sqlalchemy.exc import OperationalError
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


def wait_for_db(retries=10, delay=3):
    for i in range(retries):
        try:
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            print("Database is ready!")
            return
        except OperationalError:
            print(f"Database not ready, retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("Could not connect to the database after several retries.")


if __name__ == "__main__":
    wait_for_db()
    Base.metadata.create_all(bind=engine)

    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
