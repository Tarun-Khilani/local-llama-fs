# local-llama-fs

## Inspiration

This project draws inspiration from [LlamaFS](https://github.com/iyaja/llama-fs), reimagining its concept with:

- Local model implementation for enhanced privacy utilizing [Ollama](https://ollama.com/)
- Refined prompts
- Extended and easy-to-use customization options through config.py

The caveat is that it is slow depending on the local GPU availability.

## Installation

### Prerequisites

Before installing, ensure you have the following requirements:
- Python 3.10 or higher
- pip (Python package installer)

You will also need to Download the latest version of [Ollama](https://ollama.com/download)

### Installing

To install the project, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/Tarun-Khilani/local-llama-fs.git
    ```

2. Navigate to the project directory:
    ```bash
    cd local-llama-fs
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Pull the models you wish to use:
    For Vision-Language Model (Utilized for image summaries):
    ```bash
    ollama pull moondream
    ```
    For Language Model (Utilized for text summaries):
    ```bash
    ollama pull phi3
    ```
    Alternatively, you can use llama3 (8B) as well:
    ```bash
    ollama pull llama3
    ```

## Usage

To use the project, simply run the following command:
```bash
python main.py "SRC_PATH" "DST_PATH"
```

Where:

- SRC_PATH: The path to the source directory
- DST_PATH: The path to the destination directory

## License

MIT License