# YouTube Transcript Copy Assistant

A small starter project for pulling YouTube transcripts and turning them into copywriting source material.

## What this does

- Accepts a YouTube URL or video ID.
- Pulls the public transcript when captions are available.
- Saves a clean transcript file.
- Creates a copy brief with hooks, angles, objection notes, and CTA prompts you can bring back into Codex.

## Important note about the official YouTube API

The official YouTube Data API can download captions only for videos your authorized account can manage. For public videos, this starter uses publicly available transcript data instead of the official captions download endpoint.

A YouTube API key can still be useful for video metadata, search, channel data, and playlist data. Do not commit the real key to this public repo.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Add your YouTube API key

Create a local file named `.env` in the project root, next to `README.md`:

```bash
cp .env.example .env
```

Then edit `.env` so it contains your real key:

```bash
YOUTUBE_API_KEY=your_real_key_here
```

The real `.env` file is ignored by Git, so it should stay on your machine and never get pushed to GitHub.

## Usage

```bash
python transcript_to_copy.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Outputs are saved in `outputs/`.

## Copy workflow

1. Run the script with a YouTube URL.
2. Open the generated `.copy.md` file.
3. Paste that brief into Codex with the kind of copy you want: ad, email, landing page, social post, product page, or script.

## Next step

If you want this to work with your own channel through the official YouTube API, add OAuth credentials and use the captions endpoint for videos you own or manage.
