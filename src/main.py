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
        self.final_surface = pygame.display.set_mode((window_size[0]*window_scale, window_size[1]*window_scale), HWSURFACE | DOUBLEBUF)
        self.primary_surface = Surface((window_size[0], window_size[1]))
        self.collision_manager = CollisionManager()
        pygame.init()
        pygame.mixer.init()
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
            if object.layer == collision_layer or object.type == TRAPDOOR:
                to_collide.append(object)

        self.collision_manager.handle_all_collisions(to_collide)

    def render(self):
        self.primary_surface.fill(background_color)
        try:
            #TODO do better
            if [obj for obj in all_objects if obj.type == PLAYER]:
                camera_position.x, camera_position.y = [ ( obj.position.x - (window_size[0]/2) + (obj.size.x/2) , obj.position.y - (window_size[1]/2) + (obj.size.y/2) ) for obj in all_objects if obj.type == PLAYER ][0]

            #draw object in layered order
            for layer in range(min(object.layer for object in all_objects), max(object.layer for object in all_objects)+1):
                for object in all_objects:
                    if object.layer == layer:
                        self.primary_surface.blit(object.surface, (object.position.x - camera_position.x, object.position.y - camera_position.y))
        except Exception as e:
            print(f'render loop issue:\n{e}')
            pass

        self.final_surface.blit(transform.scale(self.primary_surface, self.final_surface.get_rect().size), (0, 0))
        pygame.display.flip()

    def quit(self):
        global app_running
        all_objects.clear()
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

    def exec(self, cmd):
        exec(cmd)

Thread(target=App).start()
while not app_running:
    time.sleep(0.1)
    print('initializing')
