from game_object   import *
from shared        import *

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
        self.bgcolor = (128,128,128,255)

        # object specific
        self.text       = '>'
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
            global event_receiver_objects 
            if Rect(self.position, self.size).collidepoint(pos):
                self.text = ''
                self.bgcolor = (0,0,255,255)
                if self not in event_receiver_objects:
                    event_receiver_objects.append(self)
            else:
                self.text = '>'
                self.bgcolor = (128,128,128,255)
                if self in event_receiver_objects:
                    event_receiver_objects.remove(self)

        self.animation_spritesheet.fill(self.bgcolor)
        self.animation_spritesheet.blit(self.text_font.render( self.text, False, self.text_color, self.bgcolor ), (0,0))

    def on_event(self, event, app):
        if event.type == pygame.KEYDOWN:
            print('KEYDOWN')
            if event.key == pygame.K_RETURN:
                app.exec(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_DELETE:
                self.text = ''
            else:
                self.text += event.unicode
