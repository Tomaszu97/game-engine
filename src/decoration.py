from .game_object   import *
from .shared        import *

class Decoration(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type           = DECORATION
        self.name           = 'decor'
        self.layer          = collision_layer - 1
        #TODO do animation_grid in set_animation_spritesheet
        # always set animation_grid before setting spritesheet
        self.animation_grid = [1,1]
        self.set_animation_spritesheet(resources.decoration)
        self.mass = 0

class ProgressBar(Decoration):
    pass
