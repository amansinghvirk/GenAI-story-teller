import os
import google.generativeai as genai
from vertexai.vision_models import ImageGenerationModel


class StoryImageGen:


    def __init__(self):
        genai.configure()
        self.language_model = genai.GenerativeModel(os.getenv('IMAGE_TO_TEXT_MODEL'))
        self.model = ImageGenerationModel.from_pretrained(os.getenv("VISION_MODEL"))
        self.n_retries = 1


    def generate_image(self, image_prompt):

        self.prompt = image_prompt
        while self.n_retries <= 6:
            print(f"Image generation for the story, try {self.n_retries}")
            try:
                self.image = self.model.generate_images(prompt=self.prompt)[0]
                self.n_retries = 1
                break
            except Exception as e:
                self.n_retries += 1
                print(f"Error generating image: {e}, trying again, try: {self.n_retries}")
                if self.n_retries <= 2:
                    continue
                elif (self.n_retries > 2) and (self.n_retries <=5):
                    print(f"Error generating image: {e}, trying with improved prompt, try: {self.n_retries}")
                    self.improve_prompt()
                    continue
                else:
                    raise e
        
    def improve_prompt(self):
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

        print(f"ORIGINAL_PROMPT: {self.prompt}")
        self.prompt = self.language_model.generate_content(prompt_to_lang_model).text
        print(f"IMPROVED_PROMPT: {self.prompt}")

    
    def save_image(self, image_file):
        with open(image_file, "wb") as f:
            filename = f.name
            self.image.save(filename, include_generation_parameters=False)