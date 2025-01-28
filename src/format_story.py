"""
Module for creating and formatting a story with HTML.
"""


class FormatStory:
    """
    A class to format and structure a story using HTML.

    This class allows adding a title, introduction, and multiple parts (sections)
    with images and text. The story is formatted with HTML and can be saved to a file.

    Attributes:
        background_color (str): The background color of the story.
        font_color (str): The font color for the text in the story.
        font_family (str): The font family for the text in the story.
        story_parts (str): A string containing the HTML for all the story parts.
    """

    def __init__(self, background_color, font_color, font_family):
        """
        Initializes a new FormatStory object.

        Args:
            background_color (str): The background color of the story.
            font_color (str): The font color for the text in the story.
            font_family (str): The font family for the text in the story.
        """
        self.background_color = background_color
        self.font_color = font_color
        self.font_family = font_family
        self.story_parts = "\n"

    def add_title(self, title):
        """
        Adds a title to the story.

        The title is centered and wrapped in an <h1> tag.

        Args:
            title (str): The title of the story.
        """
        self.title = f"""
            <div style="text-align: center"><h1>{title}</h1></div>
        """

    def add_introduction(self, introduction):
        """
        Adds an introduction to the story.

        The introduction is wrapped in a <p> tag.

        Args:
            introduction (str): The introduction of the story.
        """

        self.story_intro = f"""
            <p>{introduction}</p>

        """

    def add_part(self, image_path, story, section, back_color, font_color):
        """
        Adds a part (section) to the story.

        Each part includes an image and text. The layout alternates between
        having the image on the left or right based on whether the section number is even or odd.

        Args:
            image_path (str): The path to the image for this part.
            story (str): The text content for this part.
            section (int): The section number (used to alternate layout).
            back_color (str): The background color of this section.
            font_color (str): The font color of the text in this section.
        """

        if section % 2 == 0:
            part = f"""
            <div style="height: 10px"></div>
            <div style="background-color: {back_color};  margin: auto; box-shadow: 2px 2px 3px 3px {font_color}; border-radius: 25px;">
                <table style="margin: auto; color: {font_color}; table-layout: fixed; width: 980px; height: 300px; padding: 0px 0px 0px 0px; margin-left: 0px;">
                <tr style="margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;">
                <td style="margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;"><img src="../{image_path}" style="display:block; height: 300px; border-radius: 24px 0px 0px 24px; margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;" width="100%" ></td>
                <td><div style="line-height: 1.3; text-align: left; font-size: 20px; margin-left: 16px;">{story}</div></td>
        
                </tr>
                </table>
            </div>
            """
        else:
            part = f"""
            <div style="height: 10px"></div>
            <div style="background-color: {back_color};  margin: auto; box-shadow: 2px 2px 3px 3px {font_color}; border-radius: 25px;">
                <table style="margin: auto; color: {font_color}; table-layout: fixed; width: 980px; height: 300px; padding: 0px 0px 0px 0px; margin-right: 0px;">
                <tr style="margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;">
                <td><div style="line-height: 1.3; text-align: right; font-size: 20px; margin-right: 16px;">{story}</div></td>
                <td style="margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;"><img src="../{image_path}" style="display:block; height: 300px; border-radius: 0px 24px 24px 0px; margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;" width="100%" ></td>
                
                </tr>
                </table>
            </div>

            """
        self.story_parts = self.story_parts + "\n" + part

    def compile_story(self):
        """
        Compiles all the story elements into a complete HTML structure.

        This combines the title, introduction, and all story parts into a single HTML string
        that represents the complete formatted story.
        """
        self.story = f"""
                <div style="background-color: {self.background_color}; font-family: {self.font_family};
                    max-width: 1000px; padding: 10px;   margin: auto;
                    padding: 10px; box-shadow: 2px 2px 4px 4px {self.font_color}; color: {self.font_color}">
                    {self.title}
                    <div style="font-size: 20px; text-align: center;">{self.story_intro}</div>
                    {self.story_parts}
                </div>
        """

    def get_story(self):
        """
        Returns the compiled HTML story.

        Returns:
            str: The complete HTML story.
        """
        return self.story

    def save_story(self, story_path):
        """
        Saves the compiled story to an HTML file.

        Args:
            story_path (str): The path to the file where the story will be saved.
        """
        with open(story_path, "w") as f:
            f.write(f"<html>{self.story}</html>")
