from pygame			import	*
from game_object	import	*
from player			import	*
from spawner		import	*
from decoration		import	*
from label			import	*
from shared			import	*
from enemy			import	*
from tiled			import	*
from collision_manager	import *
from resource_handler	import	*
from threading 		import	Thread
import time
import random
import os
import code
import copy


class App():
	def __init__(self):
		self.children = []
		self.clock = Clock()
		self.running = True
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_position[0], window_position[1])
		self.surface = pygame.display.set_mode((window_size[0], window_size[1]), HWSURFACE | pygame.DOUBLEBUF)
		self.collision_manager = Collision_Manager()
		pygame.init()
		self.run()


	def handle_events(self, event):
		if event.type == pygame.QUIT:
			self.quit()
			

	def loop(self):
		to_collide = []

		for object in all_objects:
			# w, h = pygame.display.get_surface().get_size()
			# if not ( -object.size.x <= object.position.x <= w and -object.size.y <= object.position.y <= h ) and object.type != ObjectType.PLAYER:
			# 	object.kill()

			try:
				object.every_tick()
			except:
				pass

			if object.layer == collision_layer:
				to_collide.append(object)

		#collisions
		self.collision_manager.check_all(to_collide)

		for object in to_collide:
			if object.to_kill is True:
				try:
					object.kill()
				except:
					pass
					


	def render(self):
		self.surface.fill((70,180,255,255))
 
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
		killall()
		self.running = False
		pygame.quit()


	def run(self):
		while(self.running):
			self.loop()
			self.render()
			self.clock.tick(tick)

			for event in pygame.event.get():
				self.handle_events(event)


Thread(target=App).start()
time.sleep(1)

###########################################
#TODO music doesnt play if file imported from somewhere
#TODO replace above time.sleep to sth that makes more sense
TiledManager().load_map('../data/nice_map.tmx')

pl = Player()
tr = Trapdoor()
tr2 = Trapdoor()
tr.move(200,200)
tr2.move(200,350)
tr.reset()
tr2.reset()

def f():
	print('spawning enemies...')
	Enemy_Following(target_list = [pl], position = Vector2(200.0,400.0))
	Enemy_Following(target_list = [pl], position = Vector2(400.0,200.0))
	Enemy_Following(target_list = [pl], position = Vector2(400.0,400.0))
tr.set_handler(f)

def g():
	print('resetting tr...')
	tr.reset()
	tr2.reset()
tr2.set_handler(g)

code.interact(local=locals())