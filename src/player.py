from .game_object   import *
from .wall          import *
from .bullet        import *
from .shared        import *
from .progressbar   import *

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
        self.bullet_clock    = Clock()
        self.bullet_timer    = 0
        self.bullet_delay    = 400
        self.speed           = 1.5
        self.max_hp          = 100
        self.max_mana        = 100
        self._hpbar          = ProgressBar()
        self._hpbar.size     = Vector2(self.size.x + 4, 5)
        self._manabar        = ProgressBar()
        self._manabar.size   = Vector2(self.size.x + 4, 5)
        self._manabar.fg_color = Color(92, 108, 156,255)
        self._manabar.bg_color = Color(108, 139, 164,255)
        self.hp             = self.max_hp
        self.mana           = self.max_mana
        self.contact_damage = 0
        self.damage         = 10
        self.team = True

    def every_tick(self):
        global debug
        if debug:
            print(f'player pos: {self.position}')
        #TODO remove this - using mana bar as bullet reloading bar
        self._manabar.progress = self.bullet_timer/self.bullet_delay
        self._hpbar.position = self.position + Vector2(-2, -6)
        self._manabar.position = self.position + Vector2(-2, -12)
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

        global debug
        if debug:
            if mouse_pressed[2] and self.bullet_timer > self.bullet_delay:
                x = GameObject()
                x.move(Vector2(Vector2(pygame.mouse.get_pos())/6 - (x.size/2) + cameras[0].world_position))
                self.bullet_timer = 0

            if mouse_pressed[1] and self.bullet_timer > self.bullet_delay:
                x = Wall()
                x.move(Vector2(Vector2(pygame.mouse.get_pos())/6 - (x.size/2) + cameras[0].world_position))
                self.bullet_timer = 0
        # //

    def shoot(self):
        # create bullet in the middle of player
        bullet = Bullet(self)
        bullet.move(self.position + (self.size/2) - (bullet.size/2))

        # calculate where to shoot
        shooting_direction = Vector2(pygame.mouse.get_pos() - (Vector2(window_size)/2))
        shooting_direction = shooting_direction.normalize()
        try:
            bullet.movement_speed = shooting_direction*bullet.speed
            #TODO delete this?
            #q = Vector2()
            #q.from_polar(( self.hitbox_size.length()/2 + bullet.hitbox_size.length()/2,  shooting_direction.as_polar()[1]))
            #bullet.move(q)
        except ValueError:
            bullet.kill()

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        self._hpbar.progress = self._hp/self.max_hp

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, value):
        self._mana = value
        self._manabar.progress = self._mana/self.max_mana