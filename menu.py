from src.main import *

pygame.mixer.music.load('data/music/jump.ogg')
pygame.mixer.music.play(-1)

background = Decoration()
background.set_animation_spritesheet(pygame.image.load(basedir + 'data/images/menubg-enlarged.png').convert_alpha())
background.position = Vector2(-100,-80)

start_button = Button()
start_button.position = Vector2(0,20)
start_button.size = Vector2(80,15)
start_button.set_animation_spritesheet_blank(Color(148, 129, 110))
start_button.text_color = Color(227, 191, 95)
start_button.bg_color = Color(148, 129, 110)
start_button.text = '  start game'
def start_handler():
    global all_objects
    all_objects.clear()
    pygame.mixer.music.stop()
    import l1

start_button.handler = start_handler

quit_button = Button()
quit_button.position = Vector2(0,60)
quit_button.size = Vector2(80,15)
quit_button.set_animation_spritesheet_blank(Color(148, 129, 110))
quit_button.text_color = Color(227, 191, 95)
quit_button.bg_color = Color(148, 129, 110)
quit_button.text = '     quit'
def quit_handler():
    #TODO investigate why setting this from app thread doesnt work
    global app_running
    app_running = False
    global app_instance
    app_instance.quit()
quit_button.handler = quit_handler

title = Label()
title.size = Vector2(110,30)
title.position  = Vector2(-15,-20)
title.text_font = ('/data/fonts/m5x7.ttf', 32)
title.text = '   DING'
title2 = Label()
title2.layer -=1
title2.size = Vector2(110,30)
title2.position  = Vector2(-15,-20)
title2.bg_color, title2.text_color = title2.text_color, title2.bg_color 
title2.text_font = ('/data/fonts/m5x7.ttf', 32)
title2.text = '   DING'
title_blink_state = True

big_camera = Camera()
big_camera.world_size = Vector2(256,144)
big_camera.window_size = Vector2(big_camera.world_size*6)
big_camera.move_world(*(-Vector2(big_camera.world_size/2) + start_button.size/2))
big_camera.move_world(0,25)

#big_camera.world_size = Vector2(256*4,144*4)
#big_camera.move_world(-100,-100)

stuff = [GameObject() for _ in range(12)]
for i,o in enumerate(stuff):
    o.type = CONTAINER
    o.position = Vector2(-50,(50 * i)-400)
    o.slowdown_factor = 1
    o.movement_speed = Vector2(0,1.5)
for o in stuff:
    if random.randint(1,100) > 60:
        o.kill()
def hdlr1(trap, prey):
    prey.move(0,-400)
    trap.reset()
tr1 = Trapdoor()
tr1.move(-50, 250)
tr1.set_handler(hdlr1)

stuff2 = [GameObject() for _ in range(12)]
for i,o in enumerate(stuff2):
    o.type = CONTAINER
    o.position = Vector2(120,(-50 * i)+400)
    o.slowdown_factor = 1
    o.movement_speed = Vector2(0,-1.5)
for o in stuff2:
    if random.randint(1,100) > 60:
        o.kill()
def hdlr2(trap, prey):
    prey.move(0,400)
    trap.reset()
tr2 = Trapdoor()
tr2.move(120, -250)
tr2.set_handler(hdlr2)

stuff3 = [GameObject() for _ in range(20)]
for i,o in enumerate(stuff3):
    o.type = CONTAINER
    o.position = Vector2((50 * i)-45, (50 * i))
    o.slowdown_factor = 1
    o.movement_speed = Vector2(-1.5, -1.5)
for o in stuff3:
    if random.randint(1,100) > 75:
        o.kill()
def hdlr3(trap, prey):
    prey.movement_speed = prey.movement_speed.rotate(90)
    prey.move(5,0)
    trap.reset()
    global title_blink_state
    if title_blink_state:
        title2.layer +=2
        title_blink_state = False
    else:
        title2.layer -=2
        title_blink_state = True
    title.text = title._text
tr2 = Trapdoor()
tr2.move(-26,25)
tr2.set_handler(hdlr3)
def hdlr4(trap, prey):
    prey.movement_speed = Vector2(-1.5,-1.5)
    prey.position = Vector2(len(stuff3)*50-45,len(stuff3)*50)
    trap.reset()
tr4 = Trapdoor()
tr4.move(90,-80)
tr4.set_handler(hdlr4)

#code.interact(local=locals())
