import subprocess
import os
from pathlib import Path
import re

def extract_class_name(code: str) -> str:
    """Extract the name of the class inheriting from Scene in Manim code"""
    match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', code)
    if match:
        return match.group(1)
    return "GeneratedScene"

def render_manim_code(code_path: str) -> str:
    """Render Manim code into a video"""
    try:
        
        with open(code_path, "r", encoding="utf-8") as f:
            code = f.read()

        scene_name = extract_class_name(code)
        print(f"🎬 Rendering Scene: {scene_name}")

        
        output_dir = Path(code_path).parent

        
        command = [
            "manim",
            "-pql",  
            code_path,
            scene_name,
            "--media_dir", str(output_dir)  
        ]

        
        subprocess.run(command, check=True)

        
        rendered_video_path = list(output_dir.rglob("*.mp4"))[0]
        print(f"✅ Video Rendered: {rendered_video_path}")

        return str(rendered_video_path)

    except Exception as e:
        print("❌ Rendering failed:", e)
        return ""
