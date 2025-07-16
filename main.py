from fastapi import FastAPI, Request
from pydantic import BaseModel
import os, uuid
from utils import download_file, generate_scene, concatenate_videos

app = FastAPI()

TEMP_DIR = "/mnt/data"

class MediaItem(BaseModel):
    image_url: str
    audio_url: str
    subtitle: str

class MediaRequest(BaseModel):
    media: list[MediaItem]

@app.post("/generate")
async def generate_video(request: MediaRequest):
    scene_paths = []
    job_id = str(uuid.uuid4())
    job_dir = os.path.join(TEMP_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    for i, item in enumerate(request.media):
        img = os.path.join(job_dir, f"img_{i}.jpg")
        audio = os.path.join(job_dir, f"audio_{i}.mp3")
        scene = os.path.join(job_dir, f"scene_{i}.mp4")

        download_file(item.image_url, img)
        download_file(item.audio_url, audio)
        generate_scene(img, audio, item.subtitle, scene, i)
        scene_paths.append(scene)

    final_output = os.path.join(TEMP_DIR, "output.mp4")
    concatenate_videos(scene_paths, final_output)

    return {"video_url": "/download/output.mp4"}

@app.get("/download/{filename}")
def download(filename: str):
    path = os.path.join(TEMP_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path, media_type="video/mp4", filename=filename)
    return {"error": "file not found"}
