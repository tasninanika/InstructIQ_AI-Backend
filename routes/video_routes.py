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

@router.post("/upload_video/")
async def upload_video(file: UploadFile = File(...)):
    try:
        # Save video
        video_path = os.path.join("uploads/videos", f"temp_{file.filename}")
        with open(video_path, "wb") as f:
            f.write(await file.read())

        # Extract audio
        audio_filename = f"{file.filename.split('.')[0]}.wav"
        audio_path = os.path.join("uploads/audios", audio_filename)
        clip = mp.VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)

        # Transcription using Whisper
        transcription_result = model.transcribe(audio_path)
        transcription_text = transcription_result["text"]

        # Save to MongoDB
        video_doc = {
            "filename": file.filename,
            "video_path": video_path,
            "audio_path": audio_path,
            "transcription": transcription_text
        }
        result = videos_collection.insert_one(video_doc)

        return JSONResponse({
            "message": "Video uploaded, audio extracted & transcribed!",
            "video_file": video_path,
            "audio_file": audio_path,
            "transcription_snippet": transcription_text[:100],
            "video_id": str(result.inserted_id)
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)