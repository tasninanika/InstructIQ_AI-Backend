from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import moviepy as mp
import whisper
from database import videos_collection

router = APIRouter()

# folders 
os.makedirs("uploads/videos", exist_ok=True)
os.makedirs("uploads/audios", exist_ok=True)

# Load Whisper model
model = whisper.load_model("small")
