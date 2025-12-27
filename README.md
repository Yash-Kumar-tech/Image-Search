# Image Metadata & Search
Efficiently indexing and searching large image collections is a common challenge for professionals and enthusiasts alike. This application leverages image captioning models like—BLIP for automated caption generation and CLIP for semantic embeddings—integrated within a streamlined desktop interface. It enables users to organize, annotate, and retrieve images not only by explicit tags but also by semantic content and contextual meaning. Whether employed in academic research, creative design, or personal archiving, the system transforms extensive image repositories into structured, searchable knowledge bases.

## Features
- Indexing: Scan folders recursively and automatically generate descriptive tags + embeddings for each image.
- Semantic Search: Find images by meaning using CLIP embeddings — not just literal tag matches. (planned)
- Hybrid Search: Combine tag filters with semantic similarity for precise yet flexible results. (planned)
- Custom Tags: Add your own labels to any image for personalized organization. (planned)
- UI Highlights:
- Card‑based results grid with thumbnails, metadata, and context menus.
- Top bar with search input, search mode selector (Tag / Semantic / Hybrid), theme switcher, and quick access to indexing/tagging dialogs.
- Progress bars for indexing and tagging operations.
- Light/Dark/System themes.

## Installation
- Clone the repository:
git clone https://github.com/Yash-Kumar-tech/Image-Search.git
cd image-search
- Install dependencies:
pip install -r requirements.txt
- Dependencies include:
- Flet (UI)
- torch, transformers (BLIP)
- open_clip (CLIP)
- tqdm (progress bars)
- sqlite3 (metadata storage)
- Run the app:
python -m frontend.src.main

## Usage
Indexing Images
- Click Index in the top bar.
- Enter path to a folder containing images.
- Start indexing — progress bar shows completion.
- Each image is processed with BLIP (caption -> tags) and CLIP (embedding).
Searching
- Enter a query in the search bar.
- Choose search mode:
- Tag -> substring match in tags.
- Semantic -> embedding similarity. (Untested)
- Hybrid -> filter by tag, then rank semantically. (Untested)
- Results appear in a grid of cards showing thumbnail, path, tags, and indexed date.
- Right‑click a card for context menu: (Planned)
- Open Image
- Show in Folder
- Add Tag
Adding/Editing Tags (planned)
- Click Custom Tags in the top bar.
- Enter image path and comma‑separated tags.
- Progress bar shows completion.
- Tags are stored in the metadata database and searchable.
Themes
- Use the dropdown in the top bar to switch between System, Dark, or Light themes.

## Contributing
Pull requests and contributions are welcome!
