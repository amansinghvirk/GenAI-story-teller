

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


    def add_part(self, image_path, story, section):

        if section % 2 == 0:
            part = f'''
                <table style="table-layout: fixed; width: 1200px; height: 300px">
                <tr>
                <td><div><img src="../{image_path}" style="display:block; height: 300px" width="100%" ></div></td>
                <td><div style="line-height: 1; text-align: left; font-size: 30px">{story}</div></td>
                </tr>
                </table>
            '''
        else:
            part = f'''
                
                <table style="table-layout: fixed; width: 1200px; height: 300px">
                <tr>
                <td><div style="line-height: 1; text-align: right; font-size: 30px">{story}</div></td>
                <td><div><img src="../{image_path}" style="display:block; height: 300px" width="100%" ></div></td>
                
                </tr>
                </table>

            '''

        self.story_parts = self.story_parts + "\n" + part


    def compile_story(self):
        self.story = f'''
            <html>
                <body 
                style="background-color: {self.background_color}; 
                font-color: {self.font_color}; 
                font-family: {self.font_family};
                font-size: 30px
                ">
                <div style="max-width: 1250px; padding: 10px;   margin: auto;
                    padding: 10px; box-shadow: 10px 10px 20px 10px rgb(201, 210, 213);">
                    {self.title}
                    {self.story_intro}
                    {self.story_parts}
                </div>
                </body>
            </html>

        '''
    

    def save_story(self, story_path):
        self.compile_story()
        with open(story_path, "w") as f:
            f.write(self.story)
