import os
import argparse
from PIL import Image
from dotenv import load_dotenv
from src.gen_story import StoryGenerator
from src.story_image import StoryImageGen
from src.create_story import FormatStory
from src.theme_generator import StoryThemeGenerator


def main(
    topic: str=None, image_file: str=None,
        story_theme: str = "General", story_inspiration: str = "General"
):

    generator = StoryGenerator(story_theme=story_theme, story_inspiration=story_inspiration)
    if topic:
        generator.set_context(topic=topic)
    elif image_file:
        img = Image.open(image_file)
        generator.set_image_context(img=img)
    else:
        with open("inputs/context.txt", "r", encoding="utf-8") as f:
            context = f.read()
        generator.set_context(context=context)
    story = generator.generate_response()

    print(story.keys())
    print(story.get("style"))

    current_story_theme = ""
    for key, value in story.get("style").items():
        current_story_theme = current_story_theme + f"\n{key}: {value},"
    story_generator = StoryImageGen()
    theme_generator = StoryThemeGenerator(story_theme=current_story_theme)

    # Generate Images
    for id, story_part in story.get("story").items():
        story_generator.generate_image(image_prompt=story_part.get("image_prompt"))
        image_file_path = os.path.join("outputs", f"{id}.png")
        story_generator.save_image(image_file=image_file_path)
        theme_generator.extract_image_theme(image_file=image_file_path)
        print(f"Image saved for {id}")

    story_theme = theme_generator.get_story_theme()
    print(story_theme)

    story_formmater = FormatStory(
        background_color=story_theme.get("BackgroundColor"),
        font_color=story_theme.get("FontColor"),
        font_family=story_theme.get("FontFamily")

    )
    story_formmater.add_title(title=story.get("title"))
    story_formmater.add_introduction(introduction=story.get("introduction"))
    for id, story_part in story.get("story").items():
        image_file_path = os.path.join("outputs", f"{id}.png")
        story_formmater.add_part(
            image_path=image_file_path, story=story_part.get("story"), 
            section=int(id.split("_")[1])
        )
    
    story_formmater.save_story(os.path.join("outputs", "story.html"))


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="Generate a story")
    parser.add_argument("--topic", type=str, help="The topic of the story", default=None)
    parser.add_argument("--image", type=str, help="The image to generate a story from", default=None)
    parser.add_argument("--story_theme", type=str, help="The story output theme", default="General")
    parser.add_argument("--story_inspiration", type=str, help="The inspiration on which story theme should be based", default="General")
    args = parser.parse_args()
    main(args.topic, args.image, args.story_theme, args.story_inspiration)