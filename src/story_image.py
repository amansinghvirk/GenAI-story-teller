"""
This module provides a class for generating images based on text prompts using Google's generative AI models. 
It includes functionalities to handle retries, improve prompts, and save generated images.
"""

import os
import logging
import google.generativeai as genai
from vertexai.vision_models import ImageGenerationModel


class StoryImageGen:
    """
    A class for generating images from text prompts using Google's generative AI models.

    This class utilizes a language model to improve prompts and a vision model to generate images.
    It also handles retries and saves the generated images.
    """

    def __init__(self):
        """
        Initializes the StoryImageGen object.

        Configures the generative AI and sets up the language and vision models using environment variables.
        It also initializes the number of retries to 1.
        """
        genai.configure()
        self.language_model = genai.GenerativeModel(os.getenv("IMAGE_TO_TEXT_MODEL"))
        self.model = ImageGenerationModel.from_pretrained(os.getenv("VISION_MODEL"))
        self.n_retries = 1

    def generate_image(self, image_prompt):
        """
        Generates an image based on the provided text prompt.

        This method attempts to generate an image using the vision model.
        If the generation fails, it retries up to 6 times, potentially improving the prompt
        using the language model after the first two retries.

        Args:
            image_prompt (str): The text prompt to use for image generation.

        Raises:
             Exception: If image generation fails after maximum retries.
        """

        self.prompt = image_prompt
        while self.n_retries <= 6:
            logging.info(f"Image generation for the story, try {self.n_retries}")
            try:
                self.image = self.model.generate_images(prompt=self.prompt)[0]
                self.n_retries = 1
                break
            except Exception as e:
                self.n_retries += 1
                logging.info(
                    f"Error generating image: {e}, trying again, try: {self.n_retries}"
                )
                if self.n_retries <= 2:
                    continue
                elif (self.n_retries > 2) and (self.n_retries <= 5):
                    logging.info(
                        f"Error generating image: {e}, trying with improved prompt, try: {self.n_retries}"
                    )
                    self.improve_prompt()
                    continue
                else:
                    raise e

    def improve_prompt(self):
        """
        Improves the image generation prompt using the language model.

        This method generates a new prompt based on the original prompt to avoid generating images
        that violate responsible AI policies, include inappropriate content, or are unsuccessful.
        It logs both the original and improved prompts.
        """
        prompt_to_lang_model = f"""
            You are an professional Generative AI developer who writes prompts for vision models
            to generate the images, original prompt is provided in ORIGINAL_IMAGE_PROMPT which is not 
            able to generate the image, model is not able to generate the image. Improve the original
            prompt. 

            Rephrase the prompt, so that it should not include anything which violates and responsible AI policies,
            it should be safe to pass to model to generate the images.

            Do not include anything related to child, sexual orientation, realted to any race, image prompt should be 
            appropriate to the general audience without hurting any sentiments
            
            
            In output only provide the prompt as plain text

            ORIGINAL_IMAGE_PROMPT:
            {self.prompt}
        """

        logging.info(f"ORIGINAL_PROMPT: {self.prompt}")
        self.prompt = self.language_model.generate_content(prompt_to_lang_model).text
        logging.info(f"IMPROVED_PROMPT: {self.prompt}")

    def save_image(self, image_file):
        """
        Saves the generated image to the specified file.

        Args:
            image_file (str): The path to the file where the image should be saved.
        """
        with open(image_file, "wb") as f:
            filename = f.name
            self.image.save(filename, include_generation_parameters=False)
