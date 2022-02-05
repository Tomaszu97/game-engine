from .game_object   import *
from .shared        import *

class Label(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type            = LABEL
        self.name            = 'label'
        self.layer = collision_layer + 10

        #object specific
        self.bg_color = Color(148, 129, 110, 255)
        self.text_color = Color(227, 191, 95, 255)
        self._text = 'label'
        self.text_font = ('/data/fonts/m5x7.ttf', 16)

        self.set_animation_spritesheet_blank(self.bg_color)

    @property
    def text_font(self):
        return self._text_font

    @text_font.setter
    def text_font(self, font_path_size_tuple):
        self._text_font  = Font(basedir + font_path_size_tuple[0], font_path_size_tuple[1])
        self.text = self._text

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, text):
        self._text = text
        self.set_animation_spritesheet_blank(self.bg_color)
        words = [word.split(' ') for word in text.splitlines()]
        space = self.text_font.size(' ')[0]
        max_width, max_height = self.animation_spritesheet.get_size()
        pos = (0,0)
        x, y = pos
        for line in words:
            for word in line:
                word_surface = self.text_font.render(word, False, self.text_color, self.bg_color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                self.animation_spritesheet.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height
