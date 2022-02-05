from .game_object   import *
from .shared        import *

class Trapdoor(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type = TRAPDOOR
        self.name = 'trapdoor'
        self.layer = collision_layer - 1
        self.animation_grid = [1,1]
        global debug
        if debug:
            self.set_animation_spritesheet(resources.trapdoor)
        else:
            self.set_animation_spritesheet_blank(Color(0,0,0,0))
        self.mass = 0

        # object specific
        self.triggered = False
        self.handler = self.default_handler

    # runs when player enters trapdoor
    def trap_trigger(self, other_obj):
        if not self.triggered:
            self.triggered = True
            self.handler(self, other_obj)

    # resets trapdoor
    def reset(self):
        self.triggered = False

    # set handler function run when trapdoor triggers
    def set_handler(self, handler):
        self.handler = handler

    # default trapdoor handler
    def default_handler(self, obj, other_obj):
        print('TRAPDOOR: default trapdoor handler triggered')
