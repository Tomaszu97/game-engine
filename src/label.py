from game_object   import *
from shared        import *

class Label(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type            = ObjectType.LABEL
        self.name            = 'label'
        self.animation_grid  = [1,1]
        self.animation_speed = 4
        self.set_animation_spritesheet(resources.label)
        self.set_hitbox_offset(12)
        self.layer = collision_layer
        
        #object specific
        self.text = 'Sample Text'
        
        #collision overwrite
        self.is_collideable[ObjectType.NULL]       = False
        self.is_collideable[ObjectType.PLAYER]     = False
        self.is_collideable[ObjectType.ALLY]       = False
        self.is_collideable[ObjectType.ENEMY]      = False
        self.is_collideable[ObjectType.SPAWNER]    = False
        self.is_collideable[ObjectType.BULLET]     = False
        self.is_collideable[ObjectType.CONTAINER]  = False
        self.is_collideable[ObjectType.DECORATION] = False
        self.is_collideable[ObjectType.LABEL]      = False
        self.is_collideable[ObjectType.WALL]       = False
        self.is_collideable[ObjectType.TRAPDOOR]   = False
        self.is_collideable[ObjectType.DIALOG]     = False
