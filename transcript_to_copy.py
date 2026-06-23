#!/usr/bin/env python3
"""Pull a YouTube transcript and create a copywriting brief."""

from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(value: str) -> str:
    """Return a YouTube video ID from a URL or raw ID."""
    value = value.strip()

    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value

    parsed = urlparse(value)
    host = parsed.netloc.lower().replace("www.", "")

    if host == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]
        if video_id:
            return video_id

    if host in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
        query_video_id = parse_qs(parsed.query).get("v", [""])[0]
        if query_video_id:
            return query_video_id

        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) >= 2 and parts[0] in {"shorts", "embed", "live"}:
            return parts[1]

    raise ValueError("Please provide a valid YouTube URL or 11-character video ID.")


def fetch_transcript(video_id: str, languages: list[str]) -> list[dict]:
    transcript = YouTubeTranscriptApi().fetch(video_id, languages=languages)
    return transcript.to_raw_data()


def format_timestamp(seconds: float) -> str:
    total_seconds = int(seconds)
    minutes, secs = divmod(total_seconds, 60)
    hours, mins = divmod(minutes, 60)
    if hours:
        return f"{hours:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


def transcript_as_text(items: list[dict]) -> str:
    lines = []
    for item in items:
        timestamp = format_timestamp(float(item.get("start", 0)))
        text = " ".join(str(item.get("text", "")).split())
        if text:
            lines.append(f"[{timestamp}] {text}")
    return "\n".join(lines) + "\n"


def plain_transcript(items: list[dict]) -> str:
    return " ".join(
        " ".join(str(item.get("text", "")).split())
        for item in items
        if item.get("text")
    )


def build_copy_brief(video_id: str, transcript_text: str) -> str:
    excerpt = transcript_text[:5000]
    return textwrap.dedent(
        f"""\
        # Copy Brief From YouTube Transcript

        Video ID: `{video_id}`

        ## Source Transcript Excerpt

        {excerpt}

        ## Copy Prompts

        Use the transcript to extract:

        - 10 punchy hooks.
        - The main promise or transformation.
        - The audience pain points.
        - The objections or doubts the viewer may have.
        - The strongest proof points or examples.
        - 5 ad angles.
        - 5 email subject lines.
        - 3 landing page headline options.
        - A short CTA that feels natural to the source material.

        ## Notes

        Keep the final copy specific to the language, problems, and phrases used in the transcript. Avoid generic hype.
        """
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch a YouTube transcript and create copywriting source files."
    )
    parser.add_argument("video", help="YouTube URL or video ID")
    parser.add_argument(
        "--language",
        "-l",
        action="append",
        default=None,
        help="Transcript language code. Can be used more than once. Defaults to en.",
    )
    parser.add_argument(
        "--out",
        default="outputs",
        help="Output directory. Defaults to outputs.",
    )
    args = parser.parse_args()

    languages = args.language or ["en"]
    video_id = extract_video_id(args.video)
    transcript_items = fetch_transcript(video_id, languages)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    timed_text = transcript_as_text(transcript_items)
    plain_text = plain_transcript(transcript_items)

    transcript_path = out_dir / f"{video_id}.transcript.txt"
    clean_path = out_dir / f"{video_id}.clean.txt"
    brief_path = out_dir / f"{video_id}.copy.md"

    transcript_path.write_text(timed_text, encoding="utf-8")
    clean_path.write_text(plain_text + "\n", encoding="utf-8")
    brief_path.write_text(build_copy_brief(video_id, plain_text), encoding="utf-8")

    print(f"Saved timed transcript: {transcript_path}")
    print(f"Saved clean transcript: {clean_path}")
    print(f"Saved copy brief: {brief_path}")


if __name__ == "__main__":
    main()
