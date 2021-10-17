from pygame            import *
from pygame.time       import *
from pygame.key        import *
from pygame.sprite     import *
from pygame.surface    import *
from pygame.font       import *
from shared            import *
import copy

# object types
NULLOBJ     = 0
PLAYER      = 1
ALLY        = 2
ENEMY       = 3
SPAWNER     = 4
BULLET      = 5
CONTAINER   = 6
DECORATION  = 7
LABEL       = 8
WALL        = 9
TRAPDOOR    = 10
DIALOG      = 11
TEXTINPUT   = 12


class GameObject(Sprite):
    #set default values, handlers, textures etc.
    def __init__(self, parent=None, position = Vector2(0.0, 0.0)):
        super().__init__()

        # identity related
        self.name               = 'object'
        self.type               = NULLOBJ
        self.parent             = parent
        self.children           = []

        # size/position related
        self.rotation           = 0.0
        self.position           = Vector2(position)
        self.size               = Vector2(0.0, 0.0)
        self.hitbox_position    = Vector2(0.0, 0.0)
        self.hitbox_size        = Vector2(0.0, 0.0)
        self.hitbox_offset      = 0.0

        # look related
        self.surface            = Surface((self.size[0],self.size[1]), pygame.SRCALPHA, 32)
        self.font               = Font(f'{BASEDIR}/../data/fonts/terminus-ttf-4.49.1/TerminusTTF-4.49.1.ttf', 12)
        self.bgcolor            = Color(0,0,0,0)

        # movement related
        self.movement_speed         = Vector2(0,0)
        self.movement_acceleration  = Vector2(0,0)
        self.movement_angular_speed = 0.0
        self.slowdown_factor        = slowdown_factor

        # animation related
        self.animation_spritesheet  = Surface((self.size[0],self.size[1]), pygame.SRCALPHA, 32)
        self.animation_grid         = [1,1]   #tracks, frames
        self.animation_speed        = 4       #ticks per frame
        self.animation_frame        = 0
        self.animation_track        = 0
        self.animation_counter      = 0
        self.animation_paused       = False

        # collision behavior
        self.mass               = 1000
        self.layer              = collision_layer
        self.team               = None        # for bullets (team None - neutral, True - friendly, False - enemy)
        self.is_invincible      = False       # can't be hit

        # append object to children list and all object list
        if self.parent != None:
            self.parent.children.append(self)
        all_objects.append(self)

        # initial look
        self.set_animation_spritesheet(resources.smallcrate)

        # flag for multithreading
        self.ready = True

    # move object on main surface
    def move(self, firstarg=None, secondarg=None):
        if secondarg == None:
            self.position += firstarg
        else:
            self.position += Vector2(firstarg, secondarg)

        self.hitbox_position = self.position + Vector2(self.hitbox_offset, self.hitbox_offset)

    # update animation, position, speed, acceleration
    def every_tick(self):
        try:
            self.ready
        except:
            return

        # animate
        self.animation_counter += 1
        if(self.animation_counter >= self.animation_speed):
            self.animation_counter = 0

            # every frame
            if not self.animation_paused:
                self.animation_frame += 1
                if(self.animation_frame >= self.animation_grid[1]):
                    self.animation_frame = 0;

            # redraw spritesheet to self.surface (+ optional hitbox + optional border)
            self.surface.fill(self.bgcolor)
            self.surface.blit(self.animation_spritesheet, (0,0), Rect(self.size.x*self.animation_frame, self.size.y*self.animation_track, self.size.x, self.size.y))

            if display_borders:
                draw.rect(self.surface, Color(255,255,0,255), Rect(0,0,self.size.x, self.size.y), 1)
            if display_hitboxes:
                draw.rect(self.surface, Color(255,0,0,255), Rect(self.hitbox_offset, self.hitbox_offset, self.hitbox_size.x, self.hitbox_size.y) , 1)
            if display_names:
                self.surface.blit(self.font.render( self.name, False, Color(0,255,0,255), Color(0,0,255,80) ), (0,0))
            if display_velocity:
                draw.line(self.surface, Color(0,0,255,255), self.size/2, (self.size/2)+self.movement_speed, 1) 

        #accelrate, break a bit and move
        self.movement_speed += self.movement_acceleration
        self.movement_speed *= self.slowdown_factor
        self.move(self.movement_speed)

    # constrain value in between range
    def constrain(self,val, min_val, max_val):
        return min(max_val, max(min_val, val))

    ## SIZE AND HITBOX ##

    def set_size(self, size):
        self.size = size
        self.set_hitbox_offset(self.hitbox_offset)

    # set difference between object size and its hitbox
    def set_hitbox_offset(self, offset):
        self.hitbox_offset = offset
        self.hitbox_position = self.position + Vector2(offset, offset)
        self.hitbox_size = self.size - Vector2(2*offset, 2*offset)

    def set_animation_spritesheet_blank(self, color=Color(0,0,0,255)):
        self.animation_stop()
        self.animation_grid = [1,1]
        self.animation_spritesheet = Surface((self.size[0],self.size[1]), pygame.SRCALPHA, 32)
        self.animation_spritesheet.fill(color)
        self.surface = Surface((self.size[0],self.size[1]), pygame.SRCALPHA, 32)

    # change spritesheet
    def set_animation_spritesheet(self, spritesheet):
        if isinstance(spritesheet, Surface):
            self.animation_spritesheet = spritesheet
        else:
            self.animation_spritesheet = pygame.image.load(spritesheet).convert_alpha()
        self.set_size(Vector2(self.animation_spritesheet.get_rect().width/self.animation_grid[1], self.animation_spritesheet.get_rect().height/self.animation_grid[0]))
        self.surface = Surface((self.size.x, self.size.y), pygame.SRCALPHA, 32)

    # change animation
    def change_animation_track(self, track_number):
        if track_number < self.animation_grid[0] and track_number >= 0:
            self.animation_track = track_number

    # stop animation and go back to first frame
    def animation_stop(self):
        self.animation_paused = True
        self.animation_frame = 0

    # pause animation without going back to first frame
    def animation_pause(self):
        self.animation_paused = True

    # resume animation
    def animation_play(self):
        self.animation_paused = False

    # delete object
    def kill(self):
        try:
            if self.parent != None:
                self.parent.children.remove(self)
            all_objects.remove(self)
        except ValueError:
            return

    #TODO - do this
    # returns a copy of this object
    def copy(self):
        copyobj = GameObject()
        for attr in self.__dict__:
            copyattr = getattr(copyobj, attr)
            selfattr = getattr(self, attr)

            if type(getattr(self, attr)).__name__ == 'Font':     # dont copy font
                print('WARNING: fonts arent copied during object copy')
            elif hasattr(getattr(self, attr), 'copy') and callable(getattr(getattr(self, attr), 'copy')):       #if attribute has copy method then use it
                copyattr = selfattr.copy()
            else:   # in other case use deepcopy
                copyattr = copy.deepcopy(selfattr)

        return copyobj

    def on_event(self):
        pass


