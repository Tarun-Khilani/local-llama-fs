from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.node_parser import TokenTextSplitter

from app.config import Config
from app.utils import timeit

@timeit
def load_documents(path: str):
    reader = SimpleDirectoryReader(
        input_dir=path,
        recursive=True,
        required_exts=Config.ReaderExtensions,
    )
    splitter = TokenTextSplitter(chunk_size=Config.SplitterChunkSize)
    documents = []
    for docs in reader.iter_data():
        # By default, llama index split files into multiple "documents"
        if len(docs) > 1:
            # So we first join all the document contexts, then truncate by token count
            text = splitter.split_text("\n".join([d.text for d in docs]))
            if text:
                text = text[0]
            else:
                print(f"No text found for document: {docs[0].metadata}")
                continue
            documents.append(Document(text=text, metadata=docs[0].metadata))
        else:
            documents.append(docs[0])
    print(f"Loaded {len(documents)} documents from {path}")
    return documents