from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import moviepy.editor as mp
import os
from routes import video_routes
from database import videos_collection

app = FastAPI()

# Include router
app.include_router(video_routes.router, prefix="/videos")

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


    # Save metadata to MongoDB
    video_doc = {
        "filename": file.filename,
        "video_path": video_path,
        "audio_path": audio_path
    }
    result = videos_collection.insert_one(video_doc)

    # Return response
    return JSONResponse({
        "message": "Video uploaded & audio extracted successfully!",
        "video_file": video_path,
        "audio_file": audio_path,
        "video_id": str(result.inserted_id)
    })
