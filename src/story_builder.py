"""
This module provides functionality to generate a story, including text and images, based on a given context or image.
It uses several helper classes to generate the story text, images, themes, and finally formats it to html.
"""

import os
import logging
from PIL import Image
from src.gen_story import StoryGenerator
from src.story_image import StoryImageGen
from src.format_story import FormatStory
from src.theme_generator import StoryThemeGenerator

MAX_WORDS = 2000


def build_story(
    image_file: str = None,
    context: str = None,
    story_theme: str = "General",
    story_inspiration: str = "General",
    n_words: int = 200,
):
    """
    Builds a story by generating text, images, and formatting it into HTML.

    Args:
        image_file (str, optional): Path to an image file to use as context for the story. Defaults to None.
        context (str, optional): Text context to use for the story if no image is provided. Defaults to None.
        story_theme (str, optional): The theme of the story. Defaults to "General".
        story_inspiration (str, optional): The inspiration for the story. Defaults to "General".
        n_words (int, optional): The desired number of words for the story. Defaults to 200.

    Returns:
        str: An HTML string representing the generated story.
    """

    if n_words > MAX_WORDS:
        n_words = MAX_WORDS
    generator = StoryGenerator(
        story_theme=story_theme, story_inspiration=story_inspiration, n_words=n_words
    )

    if image_file:
        img = Image.open(image_file)
        generator.set_image_context(img=img)
    else:
        generator.set_context(context=context)
    story = generator.generate_response()

    current_story_theme = ""
    for key, value in story.get("style").items():
        current_story_theme = current_story_theme + f"\n{key}: {value},"
    story_generator = StoryImageGen()
    theme_generator = StoryThemeGenerator(story_theme=story.get("theme"))

    # Generate Images
    for id, story_part in story.get("story").items():
        story_generator.generate_image(image_prompt=story_part.get("image_prompt"))
        image_file_path = os.path.join("static", "images", f"{id}.png")
        story_generator.save_image(image_file=image_file_path)
        theme_generator.extract_image_theme(image_file=image_file_path)
        logging.info(f"Image saved for {id}")

    story_theme = theme_generator.get_story_theme()
    logging.info(story_theme)
    logging.info(story_theme is None)

    logging.info(story_theme)
    story_formmater = FormatStory(
        background_color=story_theme.get("BackgroundColor"),
        font_color=story_theme.get("FontColor"),
        font_family=story_theme.get("FontFamily"),
    )
    story_formmater.add_title(title=story.get("title"))
    story_formmater.add_introduction(introduction=story.get("introduction"))
    for id, story_part in story.get("story").items():
        idx = int(id.split("_")[1])
        image_file_path = os.path.join("static", "images", f"{id}.png")

        story_part_clean = story_part.get("story").encode("utf-8", "ignore")
        story_part_clean = story_part_clean.decode()
        story_formmater.add_part(
            image_path=image_file_path,
            story=story_part_clean,
            section=idx,
            back_color=story_theme.get("BackgroundColor"),
            font_color=story_theme.get("FontColor"),
        )

    story_formmater.compile_story()

    html_story = story_formmater.get_story()

    return html_story
