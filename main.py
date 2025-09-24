from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import moviepy.editor as mp
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "InstructIQ AI backend is running!"}


@app.post("/upload_video/")
async def upload_video(file: UploadFile = File(...)):
    # Save uploaded video temporarily
    video_path = f"temp_{file.filename}"
    with open(video_path, "wb") as f:
        f.write(await file.read())

    # Extract audio from video
    audio_path = f"{file.filename.split('.')[0]}.wav"
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)

    # Return response
    return JSONResponse({
        "message": "Video uploaded & audio extracted successfully!",
        "video_file": video_path,
        "audio_file": audio_path
    })