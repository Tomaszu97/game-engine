from .game_object   import *
from .wall          import *
from .bullet        import *
from .shared        import *

class Player(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type = PLAYER
        self.name = 'player'
        self.animation_grid = [4,8]
        self.set_animation_spritesheet(resources.player_small_pixel)
        self.mass = 700
        self.layer = collision_layer
        self.hitbox_size = Vector2(self.size.x, 5)
        self.set_scaled_hitbox_offset(4)
        self.animation_speed = 6

        # object specific
        #TODO: add formulas for attack damage
        self.bullet_clock = Clock()
        self.bullet_timer = 0
        self.bullet_delay = 150
        self.speed              = 1.5
        self.hp                 = 100
        self.mana               = 100
        self.contact_damage     = 0
        self.damage             = 25

        self.team = True

    def every_tick(self):
        self.bullet_clock.tick()
        self.bullet_timer += self.bullet_clock.get_time()
        self.handle_input()
        return super().every_tick()


    def handle_input(self):
        pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        speed_vector = Vector2(0.0,0.0)

        any = False
        if pressed[pygame.K_w]:
            speed_vector.y -= self.speed
            self.change_animation_track(1)
            any = True

        if pressed[pygame.K_s]:
            speed_vector.y += self.speed
            self.change_animation_track(0)
            any = True

        if pressed[pygame.K_a]:
            speed_vector.x -= self.speed
            self.change_animation_track(2)
            any = True

        if pressed[pygame.K_d]:
            speed_vector.x += self.speed
            self.change_animation_track(3)
            any = True

        if pressed[pygame.K_o]:
            self.change_animation_track(4)
            any=True

        if pressed[pygame.K_p]:
            self.change_animation_track(5)
            any=True

        if speed_vector != (0, 0):
            speed_vector = speed_vector.normalize() * self.speed
        self.movement_speed = speed_vector

        if any:
            self.animation_play()
        else:
            self.animation_stop()

        if mouse_pressed[0] and self.bullet_timer > self.bullet_delay:
            self.shoot()
            self.bullet_timer = 0

        # TODO remove those development features
        if mouse_pressed[2] and self.bullet_timer > self.bullet_delay:
            x = GameObject()
            x.move(Vector2(Vector2(pygame.mouse.get_pos())/window_scale - (x.size/2) + camera_position))
            self.bullet_timer = 0

        if mouse_pressed[1] and self.bullet_timer > self.bullet_delay:
            x = Wall()
            x.move(Vector2(Vector2(pygame.mouse.get_pos())/window_scale - (x.size/2) + camera_position))
            self.bullet_timer = 0
        # //

    def shoot(self):
        # create bullet in the middle of player
        bullet = Bullet(self)
        bullet.move(self.position + (self.size/2) - (bullet.size/2))

        # calculate where to shoot
        shooting_direction = Vector2(pygame.mouse.get_pos() - (Vector2(window_size)*window_scale/2))
        shooting_direction = shooting_direction.normalize()
        try:
            bullet.movement_speed = shooting_direction*bullet.speed
            #TODO delete this?
            #q = Vector2()
            #q.from_polar(( self.hitbox_size.length()/2 + bullet.hitbox_size.length()/2,  shooting_direction.as_polar()[1]))
            #bullet.move(q)
        except ValueError:
            bullet.kill()
