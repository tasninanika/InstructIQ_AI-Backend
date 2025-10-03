from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import moviepy as mp
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "InstructIQ AI backend is running!"}


@app.post("/upload_video/")
async def upload_video(file: UploadFile = File(...)):
    # Ensure folders exist
    os.makedirs("uploads/videos", exist_ok=True)
    os.makedirs("uploads/audios", exist_ok=True)

    # Save uploaded video
    video_path = os.path.join("uploads/videos", f"temp_{file.filename}")
    with open(video_path, "wb") as f:
        f.write(await file.read())

    # Extract audio
    audio_filename = f"{file.filename.split('.')[0]}.wav"
    audio_path = os.path.join("uploads/audios", audio_filename)
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)

    # Return response
    return JSONResponse({
        "message": "Video uploaded & audio extracted successfully!",
        "video_file": video_path,
        "audio_file": audio_path
    })
