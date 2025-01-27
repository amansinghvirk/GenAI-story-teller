

class FormatStory:

    def __init__(self, background_color, font_color, font_family):
        self.background_color = background_color
        self.font_color = font_color
        self.font_family = font_family
        self.story_parts = "\n"

    def add_title(self, title):
        self.title = f'''
            <div style="text-align: center"><h1>{title}</h1></div>
        '''

    def add_introduction(self, introduction):
        self.story_intro = f'''
            <p>{introduction}</p>

        '''


    def add_part(self, image_path, story, section, back_color, font_color):

        if section % 2 == 0:
            part = f'''
            <div style="height: 10px"></div>
            <div style="background-color: {back_color};  margin: auto; box-shadow: 2px 2px 3px 3px {font_color}; border-radius: 25px;">
                <table style="margin: auto; color: {font_color}; table-layout: fixed; width: 980px; height: 300px; padding: 0px 0px 0px 0px; margin-left: 0px;">
                <tr style="margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;">
                <td style="margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;"><img src="../{image_path}" style="display:block; height: 300px; border-radius: 24px 0px 0px 24px; margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;" width="100%" ></td>
                <td><div style="line-height: 1.3; text-align: left; font-size: 20px; margin-left: 16px;">{story}</div></td>
        
                </tr>
                </table>
            </div>
            '''
        else:
            part = f'''
            <div style="height: 10px"></div>
            <div style="background-color: {back_color};  margin: auto; box-shadow: 2px 2px 3px 3px {font_color}; border-radius: 25px;">
                <table style="margin: auto; color: {font_color}; table-layout: fixed; width: 980px; height: 300px; padding: 0px 0px 0px 0px; margin-right: 0px;">
                <tr style="margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;">
                <td><div style="line-height: 1.3; text-align: right; font-size: 20px; margin-right: 16px;">{story}</div></td>
                <td style="margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;"><img src="../{image_path}" style="display:block; height: 300px; border-radius: 0px 24px 24px 0px; margin: 0px 0px 0px 0px; padding: 0px 0px 0px 0px;" width="100%" ></td>
                
                </tr>
                </table>
            </div>

            '''
        self.story_parts = self.story_parts + "\n" + part


    def compile_story(self):
        self.story = f'''
                <div style="background-color: {self.background_color}; font-family: {self.font_family};
                    max-width: 1000px; padding: 10px;   margin: auto;
                    padding: 10px; box-shadow: 2px 2px 4px 4px {self.font_color}; color: {self.font_color}">
                    {self.title}
                    {self.story_intro}
                    {self.story_parts}
                </div>
        '''

    def get_story(self):
        return self.story
    

    def save_story(self, story_path):
        with open(story_path, "w") as f:
            f.write(f"<html>{self.story}</html>")
