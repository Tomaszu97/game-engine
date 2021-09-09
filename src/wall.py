from game_object   import *
from shared        import *

class Wall(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type = ObjectType.WALL
        self.name = 'wall'
        self.layer = collision_layer
        self.animation_grid         =   [1,1]
        self.set_animation_spritesheet(resources.smallwall)
        self.mass = 0

        #collision overwrite
        self.is_collideable[ObjectType.NULL]       = True
        self.is_collideable[ObjectType.PLAYER]     = True
        self.is_collideable[ObjectType.ALLY]       = True
        self.is_collideable[ObjectType.ENEMY]      = True
        self.is_collideable[ObjectType.SPAWNER]    = False
        self.is_collideable[ObjectType.BULLET]     = True
        self.is_collideable[ObjectType.CONTAINER]  = False
        self.is_collideable[ObjectType.DECORATION] = False
        self.is_collideable[ObjectType.LABEL]      = False
        self.is_collideable[ObjectType.WALL]       = False
        self.is_collideable[ObjectType.TRAPDOOR]   = False
        self.is_collideable[ObjectType.DIALOG]     = False

        self.process_collision[ObjectType.NULL]    = [self.bounce]
        self.process_collision[ObjectType.PLAYER]  = [self.bounce]
        self.process_collision[ObjectType.ALLY]    = [self.bounce]
        self.process_collision[ObjectType.ENEMY]   = [self.bounce]
        self.process_collision[ObjectType.BULLET]  = [self.bounce]
