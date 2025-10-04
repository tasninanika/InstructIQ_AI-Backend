from fastapi import APIRouter
import whisper

router = APIRouter()

# Load Whisper model
model = whisper.load_model("small")

