from copy import deepcopy
import json
import ollama

from app.config import Config
from app.prompts.tree_generator import TREE_GENERATOR
from app.utils import timeit

@timeit
def generate_file_tree(summaries: list):
    client = ollama.Client()
    PROMPT = deepcopy(TREE_GENERATOR)
    PROMPT[-1]["content"] = PROMPT[-1]["content"].format(SUMMARIES = json.dumps(summaries))
    chat_completion = client.chat(
        messages=PROMPT,
        model=Config.LLM,
        format='json',
        options={"temperature": Config.DefaultTemperature},
    )

    file_tree = json.loads(chat_completion["message"]["content"])["files"]
    return file_tree
