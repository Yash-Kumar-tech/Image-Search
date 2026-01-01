# AI Image Search & Manager

A modern desktop application for indexing, searching, and managing large image collections using state-of-the-art Vision-Language Models (VLMs).

## Concept
Managing thousands of images requires more than just file names. This application uses AI models like **Qwen3-VL** and **Florence-2** to "look" at your photos, generate descriptive captions, and extract semantic features. This allows you to search your library by meaning (e.g., "a person wearing a red hat @sunset") rather than just manually assigned keywords.

## Key Features
- **Multi-Model Support**: Switch between the powerful **Qwen3-VL-2B** (high quality) and the lightweight **Florence-2-Base** (high speed) depending on your hardware and needs. 
- **Intelligent Indexing**:
    - **Automated Captioning**: Generates detailed descriptions for every image.
    - **Smart Tagging**: Uses NLP (spaCy) to extract relevant nouns and features as searchable tags.
    - **Folder Synchronization**: Scans for new, updated, or deleted images and keeps your database in sync.
- **Advanced Search**:
    - **Semantic Search**: Find images by describing their content in natural language.
    - **Hybrid Search**: Combine literal tag matching with semantic ranking for pinpoint accuracy.
- **Custom Tag Management**:
    - **Manual Edits**: Right-click any result to manually add, remove, or correct tags.
    - **Global Manager**: A central hub to browse and batch-edit metadata for all indexed images.
- **Performance Optimized**:
    - **VRAM Aware**: Automatically resizes images and clears GPU cache to prevent out-of-memory errors.
    - **Async Search**: Non-blocking search execution with visual progress feedback.
- **Modern UI**: Built with Flet (Flutter-based) featuring a sleek, responsive design with support for System/Light/Dark themes.

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Yash-Kumar-tech/Image-Search.git
cd image-search
```

### 2. Set up environment
It is recommended to use a virtual environment (Conda or venv).
```bash
# Example with venv
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application
Launch the application from the project root using:
```bash
python -m frontend.src.main
```

## Usage
1. **Initialize**: The first launch will download the required AI models (weights are cached locally).
2. **Index Folders**: Click the **Add Photo** icon in the top bar, select a folder, and click "Index / Sync".
3. **Search**: Type anything in the search bar. The app uses Hybrid search by default to give you the most relevant results.
4. **Manage Metadata**: 
    - Right-click search results to edit tags or open the file location.
    - Click the **Tag** icon in the top bar to open the central Metadata Manager.
5. **Settings**: Use the **Settings** icon to switch between Qwen-VL (Quality) and Florence-2 (Speed).

## Technology Stack
- **Frontend**: Flet (Python-based Flutter wrapper)
- **Backend AI**: PyTorch, Hugging Face Transformers
- **Databases**: 
    - **SQLite**: Image metadata and tags.
    - **ChromaDB**: High-dimensional vector embeddings for semantic search.
- **NLP**: spaCy (en_core_web_sm)

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---
*Created for organizing extensive image repositories into structured, searchable knowledge bases.*
