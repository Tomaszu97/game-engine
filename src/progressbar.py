
from .game_object   import *
from .shared        import *

class ProgressBar(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type            = NULLOBJ
        self.name            = 'progbar'
        self.layer = collision_layer + 10

        #object specific
        self.bg_color = Color(148, 129, 110, 255)
        self.fg_color = Color(224, 104, 76, 255)
        self._progress = 0.5

        self.set_animation_spritesheet_blank(self.bg_color)

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.animation_spritesheet.fill(self.bg_color)
        pygame.draw.rect(self.animation_spritesheet, self.fg_color, Rect(0,0, self.size.x*self._progress, self.size.y))