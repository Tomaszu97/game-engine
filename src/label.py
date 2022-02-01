from .game_object   import *
from .shared        import *

class Label(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type            = LABEL
        self.name            = 'label'
        self.animation_grid  = [1,1]
        self.animation_speed = 4
        self.set_animation_spritesheet(resources.label)
        self.set_scaled_hitbox_offset(12)
        self.layer = collision_layer
        self.text = 'label'
