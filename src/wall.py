from .game_object   import *
from .shared        import *

class Wall(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type = WALL
        self.name = 'wall'
        self.layer = collision_layer
        self.animation_grid         =   [1,1]
        self.set_animation_spritesheet(resources.smallwall)
        self.mass = 0