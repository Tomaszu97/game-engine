from pygame             import *
from .game_object       import *
from .player            import *
from .spawner           import *
from .decoration        import *
from .label             import *
from .textinput         import *
from .shared            import *
from .enemy             import *
from .tiled             import *
from .collision_manager import *
from .resource_handler  import *
from .camera            import *
from .button            import *
from .progressbar       import *
from threading          import Thread
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
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_position[0], window_position[1])
        self.final_surface = pygame.display.set_mode((window_size[0], window_size[1]), HWSURFACE | DOUBLEBUF)
        self.collision_manager = CollisionManager()
        pygame.init()
        pygame.mixer.init()
        pygame.key.set_repeat(200,60)

        pygame.display.set_caption('DING')
        Icon = pygame.image.load(basedir + '/data/images/crate.png')
        pygame.display.set_icon(Icon)

        global app_instance
        app_instance = self
        self.run()

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            global cameras
            if cameras:
                pos = cameras[0].trans_wind_to_world_pos(pos[0], pos[1])
            global mouseclick_receiver_objects
            for o in mouseclick_receiver_objects:
                if Rect(o.position, o.size).collidepoint(pos):
                    o.on_click()
        else:
            for x in event_receiver_objects:
                x.on_event(event, self)

    def loop(self):
        to_collide = []
        for o in all_objects:
            try:
                o.every_tick()
            except Exception as e:
                print(e)
            if o.layer == collision_layer or o.type == TRAPDOOR:
                to_collide.append(o)
        self.collision_manager.handle_all_collisions(to_collide)

    def render(self):
        global cameras
        for cam in cameras:
            try:
                cam.render([ o for o in all_objects if o.ready])
                self.final_surface.blit(transform.scale(cam.surface, (int(cam.window_size[0]), int(cam.window_size[1]))), (int(cam.window_position[0]), int(cam.window_position[1])))
            except Exception as e:
                print(f'rendering issue: {e}')
        pygame.display.flip()

    def quit(self):
        global all_objects
        all_objects.clear()
        global cameras
        cameras.clear()
        global app_running
        app_running = False
        pygame.quit()

    def run(self):
        global app_running
        app_running = True
        while(app_running):
            self.loop()
            self.render()
            self.clock.tick(tick)

            for event in pygame.event.get():
                self.handle_events(event)


Thread(target=App).start()
while not app_running:
    time.sleep(0.1)
    print('initializing')
