"""
Module for generating a story theme based on an image and a text description of the story theme.
"""

import os
import base64
import google.generativeai as genai
from PIL import Image
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_core.exceptions import OutputParserException


class StoryTheme(BaseModel):
    """
    Data model for representing a story's visual theme.

    Attributes:
        BackgroundColor (str): Background color for the web page.
        FontColor (str): Font color for the web page.
        FontFamily (str): Font to be used to present the story.
    """

    BackgroundColor: str = Field(
        ..., title="ComponentTheme", description="Background color for the web page"
    )
    FontColor: str = Field(
        ..., title="FinalTheme", description="Font color for the web page"
    )
    FontFamily: str = Field(
        ..., title="FinalTheme", description="Font to be used to present the story"
    )


class StoryThemeGenerator:
    """
    A class to generate a cohesive story theme based on an image and story context.

    This class uses Google's Generative AI to analyze an image and extract a color palette.
    It then uses this palette, along with the story context, to generate a unified theme including background color, font color, and font family.

    Attributes:
        image_to_text_model (genai.GenerativeModel): Google Generative AI model for image-to-text tasks.
        llm (GoogleGenerativeAI): Langchain wrapper for Google's generative AI model.
        proposed_theme (str): A string describing the theme or context of the story.
        themes (list): A list of extracted color palettes (JSON strings).
    """

    def __init__(self, story_theme):
        """
        Initializes the StoryThemeGenerator with a story context.

        Args:
            story_theme (str): A string describing the theme or context of the story.
        """
        genai.configure()
        self.image_to_text_model = genai.GenerativeModel(
            os.getenv("IMAGE_TO_TEXT_MODEL")
        )
        self.llm = GoogleGenerativeAI(model=os.getenv("IMAGE_TO_TEXT_MODEL"))
        self.proposed_theme = story_theme
        self.themes = []

    def extract_image_theme(self, image_file) -> str:
        """
        Extracts a color palette from an image file.

        This method analyzes the provided image and identifies a four-color palette,
        returning it as a JSON string in the themes list.

        Args:
            image_file (str): Path to the image file.

        Returns:
            None
        """
        self.image = Image.open(image_file)

        prompt = """
            You are an expert in web design, color theory, and user experience. Your task is to analyze a provided image and extract a harmonious color palette suitable for a webpage displaying that image alongside text content.

            **Objective:** Generate a four-color theme directly derived from the image, ensuring visual harmony, text readability, and a logical progression from dark to light. The generated theme will be used to style an HTML container where the image is placed and adjacent text content.

            **Detailed Instructions:**

            1.  **Image Analysis & Color Identification:**
                *   Examine the provided image meticulously.
                *   Identify the four most prominent colors based on area coverage within the image. Give preference to colors that define the overall image tone and are frequently used.
                *   Focus on capturing a spectrum of colors from dark to light, with each subsequent color being lighter than the previous one. Avoid selecting shades so similar that they become indistinguishable.

            2.  **Color Palette Generation:**
                *   Extract *exactly four* colors from the image, ensuring they represent a dark-to-light progression.
                *   The first color (`first`) should be the *darkest* prominent color in the image. This color will often be found in shadows, deeper tones, or as a primary background if it's a darker background.
                *   The second color (`second`) should be a *lighter* color than the first but still within the darker range of the image.
                *   The third color (`third`) should be a *lighter* color still and represent a color in the mid tone range of the image.
                *   The fourth color (`fourth`) should be the *lightest* prominent color in the image, often found in highlights, highlights or background areas if it's light. This will be best suited for background or light text usage.
                *   Ensure that color scheme shoudl have full gradient contrast fourth color should be very light compare to the first color

            3.  **JSON Output Format:**
                *   Return your results in a strict JSON format, as follows:
                    ```json
                    
                        "first": "#hexcode1",
                        "second": "#hexcode2",
                        "third": "#hexcode3",
                        "fourth": "#hexcode4"
                    
                    ```
                *   Each color must be represented by a valid six-digit hexadecimal color code (e.g., #FFFFFF, #000000, #A3B5C7). The case doesn't matter for the codes (uppercase or lowercase is acceptable).

            **Constraints and Considerations:**

            *   **Color Contrast:** While extracting colors, be mindful of contrast. Ensure that the darkest color (`first`) and the lightest color (`fourth`) have a sufficient contrast ratio, ideally this will make a good combination for text and background usage.
            *   **Readability:** The generated colors are intended for use within a webpage that will display text on these background colors. Your selection should help readability.
            *   **Avoid Duplicates:** Make sure that no two extracted colors are very similar. The purpose is to have four colors that represent a range of colors in the image.
            *   **Prioritize Larger Areas:** If multiple colors are similar in shade, but some are in larger areas and others are not prefer color used in larger area for extracting.
            *   **Focus on Image's Theme:** Ensure that the overall color scheme extracted genuinely reflects the visual theme or dominant feeling of the image.
            *   **Strict JSON:** Do not include any text outside the JSON object. Only output the valid json as described in the instructions.

            ```

            **Action:** Analyze the image I provide, following these instructions, and generate a JSON object containing the four extracted colors as described above.

        """

        self.image_prompt = [prompt, self.image]
        self.themes.append(
            self.image_to_text_model.generate_content(self.image_prompt).text
        )

    def get_story_theme(self):
        """
        Generates a unified story theme from the extracted color palette and story context.

        This method takes the color palettes extracted from images and the story context,
        then uses the LLM to select an appropriate background color, font color, and font family,
        returning the result as a `StoryTheme` object.

        Returns:
            StoryTheme: A `StoryTheme` object containing the final theme.

        Raises:
            OutputParserException: if the output is not in the format we expected.
        """
        themes = "\n, ".join(self.themes)

        prompt = """
            You are an expert web and visual designer, tasked with creating a cohesive style theme for a story based on its context and a provided color palette. Your goal is to generate a single, unified theme that can be applied to visual components within the story's presentation.

            **Instructions:**

            1.  **Contextual Theme Determination ( `THEMES_CONTEXT` Analysis):**
                *   Carefully analyze the provided `THEMES_CONTEXT` JSON object, which describes the story's setting, mood, and tone.
                *   Based on this analysis, determine whether a **"dark theme"** or **"light theme"** is most appropriate for the story's visual presentation.
                *   **Decision Criteria:**
                    *   **Dark Theme Preference:** Choose a dark theme if the story context suggests any of the following:
                        *   A nighttime setting or primarily occurring at night.
                        *   An atmosphere of mystery, suspense, fear, or sadness.
                        *   A somber or serious overall tone.
                    *   **Light Theme Preference:** Choose a light theme if the story context suggests any of the following:
                        *   A daytime setting or a generally bright atmosphere.
                        *   A cheerful, lighthearted, or comedic mood.
                        *   A positive, optimistic, or energetic tone.
                    *   **Default Theme:** If the context provides no strong cues for either a dark or light theme, default to a **light theme**.

            2.  **Color Palette Selection (`COLOR_PALETTE`):**
                *   From the provided `COLOR_PALETTE` JSON object, select *exactly two* contrasting colors.
                *   **Dark Theme Color Assignment:** If a dark theme was selected:
                    *   Assign a *darker* color from the `COLOR_PALETTE` to the `BackgroundColor` property.
                    *   Assign a *lighter, contrasting* color from the `COLOR_PALETTE` to the `FontColor` property, ensuring sufficient readability.
                *   **Light Theme Color Assignment:** If a light theme was selected:
                    *   Assign a *lighter* color from the `COLOR_PALETTE` to the `BackgroundColor` property.
                    *   Assign a *darker, contrasting* color from the `COLOR_PALETTE` to the `FontColor` property, ensuring sufficient readability.

            3.  **Font Family Selection (`FontFamily`):**
                *   Choose a widely recognized and web-safe font family name for the `FontFamily` property.
                *   Examples include, but are not limited to: "Arial", "Helvetica", "Times New Roman", "Georgia", "Verdana", "Roboto", "Open Sans".
                *   Select a font that is well-suited to the *selected theme* (light or dark) and the overall tone of the story. For example a san-serif font like "Arial" or "Helvetica" for a modern feel and serif fonts like "Times New Roman" for a more classic feel.


            4.  **Theme Synthesis:**
                *   Construct a single JSON object representing the final synthesized theme.
                *   This JSON object must have the following structure:
                    ```json
                    
                        "BackgroundColor": "...",
                        "FontColor": "...",
                        "FontFamily": "..."
                    
                    ```
                *   Each of  `BackgroundColor`, `FontColor`, and `FontFamily` should be populated with the choices you made in the previous steps.

            5. **Output Formatting:**
            *   **JSON Only:** Your entire response should *only* be the final JSON object as described in step 4. No additional text, explanations, or conversational elements are permitted outside of the JSON structure.
                *   **No Conflicts:** Avoid outputting any conflict resolutions. Conflicts should be resolved before providing a response. There should be no need for blending of colors, or explainations on the choices. 

            **Input Data:**

                THEMES_CONTEXT:
                {theme_context}

                COLOR_PALETTE:
                {color_pallete}



        """

        n_retry = 0

        while n_retry < 3:
            try:
                # Set up a parser + inject instructions into the prompt template.
                parser = JsonOutputParser(pydantic_object=StoryTheme)
                self.prompt = PromptTemplate(
                    template=prompt,
                    input_variables=["theme_context", "color_pallete"],
                    partial_variables={
                        "format_instructions": parser.get_format_instructions()
                    },
                )

                chain = self.prompt | self.llm | parser
                self.response = chain.invoke(
                    {"theme_context": self.proposed_theme, "color_pallete": themes}
                )

                if (
                    ("BackgroundColor" in self.response.keys())
                    & ("FontColor" in self.response.keys())
                    & ("FontFamily" in self.response.keys())
                ):
                    return self.response

            except OutputParserException as e:
                n_retry += 1
                continue
