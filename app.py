import os
import logging
from flask import Flask, render_template, request
from src.story_builder import build_story
from markupsafe import Markup

app = Flask(__name__)

# check if app is running locally or on Google Cloud Run
# if running locally load the environment variables 
# else set Application Default Credentials for vertexai authentication
if 'K_REVISION' in os.environ:
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS']=os.getenv("CREDENTIALS_FILE")
    logging.info("Runnning app in Cloud Run")
else:
    from dotenv import load_dotenv
    load_dotenv()
    logging.info("Runnning app locally..")

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/image', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        
        f = request.files['file'] 
        ext = f.filename.split(".")[1]

        img_path = os.path.join('static', 'images', f'upload.{ext}')
        f.save(img_path)   

        return render_template(
            "image.html",
            image=img_path
        ) 
  

@app.route('/context')
def get_story():
    return render_template(
        "context.html"
    ) 

@app.route('/contextstory')
def generate_story_from_context():
    context = request.args.get('context')
    n_words = int(request.args.get('n_words'))
    inspiration = request.args.get('inspiration')
    theme = request.args.get('theme')
    
    story = build_story(context=context, n_words=n_words, story_inspiration=inspiration, story_theme=theme)

    return render_template(
        "story.html",
        story=Markup(story)
    )

@app.route('/imagestory')
def generate_story_from_image():
    img = request.args.get('contextimg')

    n_words = int(request.args.get('n_words'))
    inspiration = request.args.get('inspiration')
    theme = request.args.get('theme')

    story = build_story(image_file=img, n_words=n_words, story_inspiration=inspiration, story_theme=theme)

    return render_template(
        "story.html",
        story=Markup(story)
    )

if __name__ == "__main__":
    logging.basicConfig(
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.DEBUG,
    )
    app.run(debug=True, host='0.0.0.0', port=8000)