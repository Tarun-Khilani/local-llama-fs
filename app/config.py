class Config:
    MaxRetries: int = 5
    DestDirName: str = "sample_output"

    VLM: str = "moondream"
    LLM: str = "llama3" # "llama3" or "phi3" or any other LLM pulled from Ollama

    ReaderExtensions = [".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg"]

    SplitterChunkSize: int = 2000
    DefaultTemperature: float = 0.0
    VLM_MaxTokens: int = 128