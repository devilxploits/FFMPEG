import os
import requests
import subprocess
import uuid

def download_file(url, out_path):
    r = requests.get(url)
    with open(out_path, "wb") as f:
        f.write(r.content)

def generate_scene(image_path, audio_path, subtitle_text, output_path, scene_num):
    drawtext = f"drawtext=text='{subtitle_text}':fontsize=24:fontcolor=white:x=(w-text_w)/2:y=h-50:box=1:boxcolor=black@0.5"
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-shortest",
        "-vf", drawtext,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-tune", "stillimage",
        "-pix_fmt", "yuv420p",
        "-s", "1280x720",
        output_path
    ]
    subprocess.run(cmd, check=True)

def concatenate_videos(scene_files, output_path):
    list_path = "/mnt/data/concat_list.txt"
    with open(list_path, "w") as f:
        for file in scene_files:
            f.write(f"file '{file}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        output_path
    ]
    subprocess.run(cmd, check=True)

