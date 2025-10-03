from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import moviepy as mp
import whisper
from database import videos_collection