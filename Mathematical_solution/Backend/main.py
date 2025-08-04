from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os
from pathlib import Path
from fastapi.responses import FileResponse
from code_generator import generate_code
from renderer import render_manim_code
from utils import create_output_folder, save_code_to_file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/videos/{folder}/{filename}")
async def serve_video(folder: str, filename: str):
    video_path = Path("manim_outputs") / folder / "videos" / "generated_scene" / filename
    if not video_path.exists():
        return {"error": "File not found"}, 404
    return FileResponse(video_path)


class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_animation(req: PromptRequest):
    prompt = req.prompt
    print(f"🧠 Received Prompt: {prompt}")

    try:
        code_str = generate_code(prompt)
        folder_path = create_output_folder()
        code_path = save_code_to_file(code_str, folder_path)
        video_path = render_manim_code(code_path)

        if not video_path:
            raise ValueError("Video rendering failed")

        path_parts = Path(video_path).parts
        manim_index = path_parts.index("manim_outputs")
        relevant_parts = path_parts[manim_index+1:]  
        
        
        scene_index = relevant_parts.index("generated_scene")
        folder_name = relevant_parts[0]  
        file_name = relevant_parts[-1]   
        
        return {
            "status": "success",
            "video_url": f"/videos/{folder_name}/{file_name}"
        }

    except Exception as e:
        print(f"❌ Error generating animation: {e}")
        return {
            "status": "error",
            "message": str(e)
        }