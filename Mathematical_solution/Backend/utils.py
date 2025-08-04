import os
from datetime import datetime

def create_output_folder(base_dir="manim_outputs") -> str:
    """
    Creates a timestamped folder to save generated code and output video.
    Returns the folder path.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_path = os.path.join(base_dir, timestamp)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def clean_code(code_str):
    
    if not isinstance(code_str, str):
        code_str = str(code_str)
    
        code_str = code_str.strip()
    if code_str.startswith("```python"):
        code_str = code_str[len("```python"):].strip()
    elif code_str.startswith("```"):
        code_str = code_str[len("```"):].strip()
    if code_str.endswith("```"):
        code_str = code_str[:-3].strip()
    return code_str


def save_code_to_file(code_str, folder_path):
    code_str = clean_code(code_str)  
    os.makedirs(folder_path, exist_ok=True)
    code_path = os.path.join(folder_path, "generated_scene.py")
    with open(code_path, "w", encoding="utf-8") as f:
        f.write(code_str)
    return code_path
