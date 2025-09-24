from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "InstructIQ AI backend is running!"}


