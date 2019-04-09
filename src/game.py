from pygame			import	*
from game_object	import	*
from player			import	*
from spawner		import	*
from decoration		import	*
from shared			import *
from threading 		import Thread
import time
import random
import os
import code


app = None
class App():
	def __init__(self):
		global app
		app = self
		self.children = []

		self.tick = tick
		self.clock = Clock()
		self.running = True
		
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_position[0], window_position[1])
		self.surface = pygame.display.set_mode((window_size[0], window_size[1]), HWSURFACE | pygame.DOUBLEBUF)
		pygame.init()
		
		self.run()


	def handle_events(self, event):
		if event.type == pygame.QUIT:
			self.quit()
			

	def loop(self):
		to_collide = []

		for object in all_objects:
			#TODO - kill object if out of bounds (except player) - rethink this
			w, h = pygame.display.get_surface().get_size()
			if not ( -object.size.x <= object.position.x <= w and -object.size.y <= object.position.y <= h ) and object.type != ObjectType.PLAYER:
				object.kill()

			#TODO - rethink this its probably ok
			try:
				object.every_tick()
			except:
				pass
				#print('ERROR: Object not yet initialized!')

			if object.layer == 0:
				to_collide.append(object)

		#collisions
		for object in to_collide:
			for other_object in to_collide:
				if object is not other_object:
					object.collide(other_object)


	def render(self):
		self.surface.fill((0,0,90,255))
 
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
		self.running = False
		pygame.quit()


	def run(self):
		while(self.running):
			self.loop()
			self.render()
			self.clock.tick(self.tick)

			for event in pygame.event.get():
				self.handle_events(event)


##global functions
def killall():
	all_objects.clear()

def quit():
	killall()
	pygame.quit()

Thread(target=App).start()
time.sleep(1)

###########################################

x = random.randint(0,3)
if x == 0:
	mixer_music.load('../data/loop.ogg')
if x == 1:
	mixer_music.load('../data/loop2.ogg')
if x == 2:
	mixer_music.load('../data/partypizza.ogg')
if x == 3:
	mixer_music.load('../data/terribleterror.ogg')
mixer_music.play(loops = -1)


# for i in range(5):
# 	f = 120*(i+1)
# 	for j in range(5):
# 		q = Decoration()
# 		q.move(Vector2(f, j*120))

# for i in range(5):
# 	f = 120*(i+1)
# 	for j in range(5):
# 		q = Decoration()
# 		q.layer = 10
# 		q.set_animation_spritesheet('../data/konon.png')
# 		q.move(Vector2(f, j*120))

# for i in range(5):
# 	f = 120*(i+1) + 200
# 	for j in range(5):
# 		q = GameObject()
# 		q.move(Vector2(f, j*120))


a = Spawner()
a.move(Vector2(300,300))


x = Player(app)
x.name = 'player1'

code.interact(local=locals())

#TODO music doesnt play if file imported from somewhere 