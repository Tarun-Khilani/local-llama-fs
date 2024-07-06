import functools
import os
import pathlib
import shutil
import time
from asciitree import LeftAligned
from asciitree.drawing import BoxStyle, BOX_LIGHT

from app.config import Config

def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time:.4f} seconds to execute.")
        return result
    return wrapper

def async_timeit(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function {func.__name__} took {execution_time:.4f} seconds to execute.")
        return result
    return wrapper

def create_file_tree(file_tree: dict, src_dir: str, dest_dir: str = Config.DestDirName) -> dict:
    BASE_DIR = pathlib.Path(dest_dir)
    BASE_DIR.mkdir(exist_ok=True)

    # Recursively create dictionary from file paths
    tree = {}
    for file in file_tree:
        parts = pathlib.Path(file["dst_path"]).parts
        current = tree
        for part in parts:
            current = current.setdefault(part, {})
    
    tree = {dest_dir: tree}

    tr = LeftAligned(draw=BoxStyle(gfx=BOX_LIGHT, horiz_len=1))
    print(tr(tree))

    # Prepend base path to dst_path
    for file in file_tree:
        file["dst_path"] = os.path.join(dest_dir, file["dst_path"])
        file["src_path"] = os.path.join(src_dir, file["src_path"])
    
    return file_tree

def save_file_tree(file_tree: dict):
    # Copy files from src_dir to dest_dir and make the directory if it doesn't exist
    for file in file_tree:
        os.makedirs(os.path.dirname(file["dst_path"]), exist_ok=True)
        shutil.copy(file["src_path"], file["dst_path"])