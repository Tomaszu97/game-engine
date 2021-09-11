from .game_object   import *
from .shared        import *

class Trapdoor(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type = TRAPDOOR
        self.name = 'trapdoor'
        self.layer = collision_layer
        self.animation_grid         =   [1,1]
        self.set_animation_spritesheet(resources.trapdoor)
        self.mass = 0

        # object specific
        self.triggered = False
        self.handler = self.default_handler

    # resets trapdoor
    def reset(self):
        self.triggered = False

    # default trapdoor handler
    def default_handler(self):
        print('TRAPDOOR: default trapdoor handler triggered')
