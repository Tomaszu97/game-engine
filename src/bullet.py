from .game_object   import *
from .shared        import *

class Bullet(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type = BULLET
        self.name = 'bullet'
        self.animation_grid         =   [1,5]   #always before setting spritesheet
        self.animation_speed        =   4
        self.set_animation_spritesheet(resources.smallbullet)
        self.set_scaled_hitbox_offset(3)
        self.layer = collision_layer
        self.mass = 1

        #object specific
        self.ttl_clock  =   Clock()
        self.ttl_timer  =   0
        self.ttl        =   2000 #ms
        self.damage     =   15
        self.speed      =   5

        self.team = parent.team

    def every_tick(self):
        #kill bullet after ttl
        self.ttl_clock.tick()
        self.ttl_timer += self.ttl_clock.get_time()
        if self.ttl_timer > self.ttl:
            self.kill()
        return super().every_tick()
