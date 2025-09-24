from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import moviepy.editor as mp
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "InstructIQ AI backend is running!"}


