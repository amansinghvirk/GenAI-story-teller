"""
This module implements a Flask web application for generating stories based on user-provided context or uploaded images.
It includes routes for rendering different web pages, handling file uploads, and generating stories using an external `build_story` function. 
It also handles logging and configuration based on whether the application is running locally or in Google Cloud Run.
"""

import os
import logging
from flask import Flask, render_template, request
from src.story_builder import build_story
from markupsafe import Markup

app = Flask(__name__)

# check if app is running locally or on Google Cloud Run
# if running locally load the environment variables
# else set Application Default Credentials for vertexai authentication
if "K_REVISION" in os.environ:
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS']=os.getenv("CREDENTIALS_FILE")
    logging.info("Runnning app in Cloud Run")
else:
    from dotenv import load_dotenv

    load_dotenv()
    logging.info("Runnning app locally..")

if not os.path.exists("logs"):
    os.mkdir("logs")

if os.path.exists("logs/logs.txt"):
    os.remove("logs/logs.txt")

logging.basicConfig(
    filename="logs/logs.txt",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)


@app.route("/")
def home():
    """
    Renders the home page.

    Returns:
        str: The rendered HTML content of the home page.
    """
    return render_template("home.html")


@app.route("/image", methods=["POST"])
def success():
    """
    Handles image uploads and renders the image display page.

    This function is triggered when a POST request is made to the '/image' route, usually with a file attached.
    It extracts the uploaded file, saves it to the 'static/images' directory, and renders the 'image.html' template, passing the path of the saved image.

    Returns:
        str: The rendered HTML content of the image display page with image path passed to the template.
    """
    if request.method == "POST":

        f = request.files["file"]
        ext = f.filename.split(".")[1]

        img_path = os.path.join("static", "images", f"upload.{ext}")
        f.save(img_path)

        return render_template("image.html", image=img_path)


@app.route("/context")
def get_story():
    """
    Renders the context input page.

     Returns:
        str: The rendered HTML content of the context input page.
    """
    return render_template("context.html")


@app.route("/contextstory")
def generate_story_from_context():
    """
    Generates a story based on user-provided text context.

    This function retrieves user inputs (context, number of words, inspiration, and theme) from the query parameters of the request.
    It then calls the `build_story` function with these parameters to generate a story.
    The generated story is then saved to `templates/story.html` and `templates/story_to_print.html` by `save_story` function
    Finally, it renders the 'story.html' template, which now contains the generated story.

    Returns:
        str: The rendered HTML content of the story display page.
    """
    context = request.args.get("context")
    n_words = int(request.args.get("n_words"))
    inspiration = request.args.get("inspiration")
    theme = request.args.get("theme")

    story = build_story(
        context=context,
        n_words=n_words,
        story_inspiration=inspiration,
        story_theme=theme,
    )

    save_story(story)
    return render_template("story.html")


@app.route("/imagestory")
def generate_story_from_image():
    """
    Generates a story based on a user-provided image file path.

    This function retrieves user inputs (image path, number of words, inspiration, and theme) from the query parameters of the request.
    It calls the `build_story` function with these parameters to generate a story.
    The generated story is then saved to `templates/story.html` and `templates/story_to_print.html` by `save_story` function
    Finally, it renders the 'story.html' template, which now contains the generated story.

     Returns:
        str: The rendered HTML content of the story display page.
    """
    img = request.args.get("contextimg")

    n_words = int(request.args.get("n_words"))
    inspiration = request.args.get("inspiration")
    theme = request.args.get("theme")

    story = build_story(
        image_file=img,
        n_words=n_words,
        story_inspiration=inspiration,
        story_theme=theme,
    )

    save_story(story)
    return render_template("story.html")


def save_story(story):
    """
    Saves the generated story to HTML files.

    This function takes the generated story as input, wraps it in HTML content and then writes to `templates/story.html`.
    It also saves the plain text content of story to `templates/story_to_print.html`.

    Args:
        story (str): The generated story text.
    """
    html = (
        """{% extends "index.html" %}\n{% block content %}\n"""
        + story
        + """\n{% endblock %}"""
    )

    with open("templates/story.html", "w") as f:
        f.write(html)

    with open("templates/story_to_print.html", "w") as f:
        f.write(story)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
