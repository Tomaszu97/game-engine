from .game_object   import *
from .shared        import *

class Bullet(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type = ObjectType.BULLET
        self.name = 'bullet'
        self.animation_grid         =   [1,5]   #always before setting spritesheet
        self.animation_speed        =   4
        self.set_animation_spritesheet(resources.smallbullet)
        self.set_hitbox_offset(3)
        self.layer = collision_layer
        self.mass = 1

        #object specific
        self.ttl_clock  =   Clock()
        self.ttl_timer  =   0
        self.ttl        =   2000 #ms
        self.damage     =   15
        self.speed      =   5

        #collision overwrite
        self.is_collideable[ObjectType.NULL]            =   False
        self.is_collideable[ObjectType.PLAYER]          =   True
        self.is_collideable[ObjectType.ALLY]            =   False
        self.is_collideable[ObjectType.ENEMY]           =   True
        self.is_collideable[ObjectType.SPAWNER]         =   False
        self.is_collideable[ObjectType.BULLET]          =   False
        self.is_collideable[ObjectType.CONTAINER]       =   False
        self.is_collideable[ObjectType.DECORATION]      =   False
        self.is_collideable[ObjectType.LABEL]           =   False
        self.is_collideable[ObjectType.WALL]            =   True
        self.is_collideable[ObjectType.TRAPDOOR]        =   False
        self.is_collideable[ObjectType.DIALOG]          =   False

        self.process_collision[ObjectType.PLAYER]       =   [self.take_damage]
        self.process_collision[ObjectType.ENEMY]        =   [self.take_damage]
        self.process_collision[ObjectType.WALL]         =   [self.bounce]

        self.team = parent.team

    #TODO - check dis
    def check_collideable(self, object):
        if self.to_kill:
            return False
        if object.type == ObjectType.BULLET or object.type == ObjectType.PLAYER:
            if object.team == self.team:
                return False
        return self.is_collideable[object.type]

    #TODO - check dis
    def take_damage(self, object, other_object):
        self.to_kill = True


    #kill bullet after ttl
    def every_tick(self):
        self.ttl_clock.tick()
        self.ttl_timer += self.ttl_clock.get_time()

        if self.ttl_timer > self.ttl:
            self.kill()
        return super().every_tick()
