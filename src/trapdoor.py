from .game_object   import *
from .shared        import *

class Trapdoor(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type = TRAPDOOR
        self.name = 'trapdoor'
        self.layer = collision_layer - 1
        self.animation_grid         =   [1,1]
        self.set_animation_spritesheet(resources.trapdoor)
        self.mass = 0

        # object specific
        self.triggered = False
        self.handler = self.default_handler

    # runs when player enters trapdoor
    def trap_trigger(self, object, other_object):
        if self.triggered:
            return
        self.triggered = True
        self.handler()

    # resets trapdoor
    def reset(self):
        self.triggered = False

    # set handler function run when trapdoor triggers
    def set_handler(self, handler):
        self.handler = handler

    # default trapdoor handler
    def default_handler(self):
        print('TRAPDOOR: default trapdoor handler triggered')
