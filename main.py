import os
import logging
import argparse
from dotenv import load_dotenv
from src.story_builder import build_story

def main(
    topic: str=None, image_file: str=None, context: str=None,
    story_theme: str = "General", story_inspiration: str = "General",
    n_words: int = 200
):

    if (topic is None) & (image_file is None) & (context is None):
        with open("inputs/context.txt", "r", encoding="utf-8") as f:
            context = "Random"

    story = build_story(topic, image_file, context, story_theme, story_inspiration, n_words)

    story_path = "/outputs/story.html"
    if not os.path.exists("outputs"):
        os.mkdir("outputs")
    with open(story_path, "w") as f:
        f.write(f"<html>{story}</html>")


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.DEBUG,
    )

    parser = argparse.ArgumentParser(description="Generate a story")
    parser.add_argument("--topic", type=str, help="The topic of the story", default=None)
    parser.add_argument("--image", type=str, help="The image to generate a story from", default=None)
    parser.add_argument("--context", type=str, help="Context from which story needs to be created", default=None)
    parser.add_argument("--story_theme", type=str, help="The story output theme", default="General")
    parser.add_argument("--story_inspiration", type=str, help="The inspiration on which story theme should be based", default="General")
    parser.add_argument("--n_words", type=int, help="Maximum number of words in the final story", default=200)
    args = parser.parse_args()
    main(args.topic, args.image, args.context, args.story_theme, args.story_inspiration, args.n_words)