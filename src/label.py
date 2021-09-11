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
        self.set_hitbox_offset(12)
        self.layer = collision_layer
        self.text = 'label'

class TextInput(GameObject):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        self.type            = TEXTINPUT
        self.name            = 'textinput'
        self.animation_grid  = [1,1]
        self.animation_speed = 1
        self.set_size(Vector2(200, 24))
        self.set_animation_spritesheet_blank(Color(0,0,255,0))
        self.set_hitbox_offset(0)
        self.layer = collision_layer + 10
        self.bgcolor = (0,0,255,255)

        # object specific
        self.text       = 'input'
        self.text_font  = Font(f'{BASEDIR}/../data/fonts/terminus-ttf-4.49.1/TerminusTTF-4.49.1.ttf', 22)
        self.text_color = Color(0,255,0,255)
        self.active     = True

        self.animation_spritesheet.blit(self.text_font.render( self.text, False, self.text_color, self.bgcolor ), (0,0))

    def every_tick(self):
        self.handle_input()
        return super().every_tick()

    def handle_input(self):
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            pos = pygame.mouse.get_pos()
            if Rect(self.position, self.size).collidepoint(pos):
                self.active = True
            else:
                self.active = False

        if self.active:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]:
                self.text += 'w'
                self.animation_spritesheet.fill(self.bgcolor)
                self.animation_spritesheet.blit(self.text_font.render( self.text, False, self.text_color, self.bgcolor ), (0,0))
            if pressed[pygame.K_q]:
                self.text = self.text[:-1]
                self.animation_spritesheet.fill(self.bgcolor)
                self.animation_spritesheet.blit(self.text_font.render( self.text, False, self.text_color, self.bgcolor ), (0,0))
