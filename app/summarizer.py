import asyncio
from copy import deepcopy
import json
import os

from llama_index.core import Document
from llama_index.core.schema import ImageDocument
import ollama
from termcolor import colored

from app.config import Config
from app.prompts.summarize_doc import SUMMARIZE_DOC
from app.prompts.summarize_image import SUMMARIZE_IMAGE
from app.utils import async_timeit

async def get_dir_summaries(docs, dir_path: str):
    summaries = await get_summaries(docs)
    # Convert path to relative path
    for summary in summaries:
        summary["file_path"] = os.path.relpath(summary["file_path"], dir_path)
    return summaries

@async_timeit
async def summarize_document(doc: dict, client: ollama.AsyncClient):
    PROMPT = deepcopy(SUMMARIZE_DOC)
    PROMPT[-1]["content"] = PROMPT[-1]["content"].format(DOC_JSON = json.dumps(doc))

    attempt = 0
    while attempt < Config.MaxRetries:
        try:
            chat_completion = await client.chat(
                messages=PROMPT,
                model=Config.LLM,
                format='json',
                options={"temperature": Config.DefaultTemperature},
            )
            break
        except Exception as e:
            print("Error status {}".format(e.status_code))
            attempt += 1
    summary = json.loads(chat_completion["message"]["content"], strict=False)
    summary["file_path"] = doc["file_path"]

    try:
        print(colored(summary["file_path"], "green"))  # Print the filename in green
        print(summary)  # Print the summary of the contents
        print("-" * 80 + "\n")  # Print a separator line with spacing for readability
    except KeyError as e:
        print(e)
        print(summary)

    return summary

@async_timeit
async def summarize_image_document(doc: ImageDocument, client: ollama.AsyncClient):
    PROMPT = SUMMARIZE_IMAGE
    PROMPT[-1]["images"] = [doc.image_path]

    attempt = 0
    while attempt < Config.MaxRetries:
        try:
            chat_completion = await client.chat(
                messages=PROMPT,
                model=Config.VLM,
                options={"num_predict": Config.VLM_MaxTokens},
            )
            break
        except Exception as e:
            print("Error status {}".format(e.status_code))
            attempt += 1

    summary = {
        "file_path": doc.image_path,
        "summary": chat_completion["message"]["content"],
    }

    print(colored(summary["file_path"], "green"))  # Print the filename in green
    print(summary["summary"])  # Print the summary of the contents
    print("-" * 80 + "\n")  # Print a separator line with spacing for readability
    return summary

async def dispatch_summarize_document(doc, client):
    if isinstance(doc, ImageDocument):
        return await summarize_image_document(doc, client)
    elif isinstance(doc, Document):
        return await summarize_document({"content": doc.text, **doc.metadata}, client)
    else:
        raise ValueError(f"Document type not supported for doc: {doc} of type: {type(doc)}")

async def get_summaries(documents):
    client = ollama.AsyncClient()
    summaries = await asyncio.gather(
        *[dispatch_summarize_document(doc, client) for doc in documents]
    )
    return summaries
