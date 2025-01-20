import os
from PIL import Image
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import base64

class StoryTheme(BaseModel):
    BackgroundColor: str = Field(..., title="BackgroundColor", description="Background color for the html page")
    FontColor:  str = Field(..., title="FontFamily", description="Font Family for the html page")
    FontFamily:  str = Field(..., title="FontColor", description="Font color for the html page")

class StoryThemeGenerator:

    def __init__(self, story_theme):
        genai.configure()
        self.image_to_text_model = genai.GenerativeModel(os.getenv('IMAGE_TO_TEXT_MODEL'))
        self.llm = GoogleGenerativeAI(model=os.getenv('IMAGE_TO_TEXT_MODEL'))
        self.themes = [story_theme]


    def extract_image_theme(self, image_file) -> str:

        self.image = Image.open(image_file)
        # with open(image_file, "rb") as f:
        #     self.image = base64.b64encode(f.read()).decode("utf-8")


        prompt = """
            You are expert web and visual designer, based on image data provided the provided image, 
            extract the theme elements which will be used for the website where image is being posted.
            Extracted theme should match the image.

            - Extract following styles elements for the base web page, background color, font-color, font-family
            - Style should enhance the image visibility
            - Image will be used with other text on the website, so font-color, font-family should be easily readable
                and aligned with image theme
            - Try to extract image background colors and other colors in context, and use them to create a blend for the theme
            - Result should be in the JSON format with keys as BackgroundColor, FontColor, FontFamily

        """

        self.image_prompt = [prompt, self.image]
        self.themes.append(self.image_to_text_model.generate_content(self.image_prompt).text)

    def get_story_theme(self):

        themes = "\n, ".join(self.themes)

        prompt = """
            You are expert web and visual designer, based on information provided in THEMES section
            regarding chosen styles for background colors, font colors and font fmaily

            - Anlayze, merge and combine to provide a single style which will be used for the website
            - Result should only contains single theme as JSON format keys as BackgroundColor, FontColor, FontFamily

        THEMES:


        """
        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=StoryTheme)
        self.prompt = PromptTemplate(
            template=prompt,
            input_variables=["THEMES"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = self.prompt | self.llm | parser
        self.response = chain.invoke(
            {"THEMES": themes}
        )

        return self.response
