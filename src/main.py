from pygame            import *
from game_object       import *
from player            import *
from spawner           import *
from decoration        import *
from label             import *
from shared            import *
from enemy             import *
from tiled             import *
from collision_manager import *
from resource_handler  import *
from threading         import Thread
import time
import random
import os
import code
import copy
import random

class App():
    def __init__(self):
        self.children = []
        self.clock = Clock()
        self.running = True
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_position[0], window_position[1])
        self.surface = pygame.display.set_mode((window_size[0], window_size[1]), HWSURFACE | pygame.DOUBLEBUF)
        self.collision_manager = CollisionManager()
        pygame.init()
        pygame.key.set_repeat(200,60)
        self.run()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.quit()
        else:
            for x in event_receiver_objects:
                x.on_event(event, self)

    def loop(self):
        to_collide = []
        for object in all_objects:
            # w, h = pygame.display.get_surface().get_size()
            # if not ( -object.size.x <= object.position.x <= w and -object.size.y <= object.position.y <= h ) and object.type != PLAYER:
            #   object.kill()
            try:
                object.every_tick()
            except Exception as e:
                print(e)
            if object.layer == collision_layer:
                to_collide.append(object)

        self.collision_manager.handle_all_collisions(to_collide)

    def render(self):
        self.surface.fill(background_color)
        try:
            #draw object in layered order
            for layer in range(min(object.layer for object in all_objects), max(object.layer for object in all_objects)+1):
                for object in all_objects:
                    if object.layer == layer:
                        self.surface.blit(object.surface, (object.position.x, object.position.y))
        except ValueError:
            pass
        pygame.display.flip()

    def quit(self):
        all_objects.clear()
        self.running = False
        pygame.quit()

    def run(self):
        while(self.running):
            self.loop()
            self.render()
            self.clock.tick(tick)

            for event in pygame.event.get():
                self.handle_events(event)

    def exec(self, cmd):
        exec(cmd)

Thread(target=App).start()
time.sleep(1)

###########################################
#TODO music doesnt play if file imported from somewhere
#TODO replace above time.sleep to sth that makes more sense

#pl = Player()
#pl.move((window_size[0]/2)-(pl.size[0]/2),(window_size[1]/2)-(pl.size[1]/2))
#pl.set_animation_spritesheet_blank(color=(0,0,0,255))
#
#gobjs=[]
#while True:
#    [ x.kill() for x in gobjs ]
#    gobjs = [GameObject() for _ in range(20)]
#    for idx,go in enumerate(gobjs):
#        noise_x = random.randint(0,150)
#        noise_y = random.randint(0,150)
#        go.move((idx%20)*45 + noise_x, -200 + (idx/20)*45 + noise_y)
#        go.set_animation_spritesheet_blank(color=(255,165,0,255))
#        go.slowdown_factor=1
#        go.movement_speed = Vector2(0, 14)
#    time.sleep(1)


TiledManager().load_map(f'{BASEDIR}/../data/maps/nice_map.tmx')
pl = Player()
pl.move(100,100)
tr = Trapdoor()
tr2 = Trapdoor()
pl.move(200,200)
tr.move(200,200)
tr2.move(200,350)
tr.reset()
tr2.reset()

def f():
    print('spawning enemies...')
    EnemyFollowing(target_list = [pl], position = Vector2(200.0,400.0))
tr.handler = f

def g():
    print('resetting tr...')
    tr.reset()
    tr2.reset()
tr2.handler = g

#ti = TextInput()

#ti.set_size(Vector2(window_size[0], 24))
#ti.set_animation_spritesheet_blank(Color(0,0,255,0))
#ti.animation_spritesheet.blit(ti.text_font.render( ti.text, False, ti.text_color, ti.bgcolor ), (0,0))
#tmp_input = ti

#code.interact(local=locals())
