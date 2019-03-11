from pygame			import	*
from game_object	import	*
from player			import	*
from spawner		import	*
from shared import *
from threading import Thread
import time

app = None

class App():
	def __init__(self):
		global app
		app = self
		self.children = []

		self.tick = 75
		self.clock = Clock()
		self.running = True
		self.surface = pygame.display.set_mode((1200, 700), HWSURFACE | pygame.DOUBLEBUF)
		pygame.init()
		
		self.run()


	def handle_events(self, event):
		if event.type == pygame.QUIT:
			self.quit()
			

	def loop(self):
		to_destroy = []
		#TODO - collide only required objects (physical = True) and do it until there are no collisions left
		for object in all_objects:
			object.every_tick()
			for other_object in all_objects:
				if object is not other_object:
					object.collide(other_object)
			
			#kill object if out of bounds (never kill player)
			w, h = pygame.display.get_surface().get_size()
			if not ( -object.size.x <= object.position.x <= w and -object.size.y <= object.position.y <= h ) and object.type != ObjectType.PLAYER:
				object.kill()


			

	def render(self):
		self.surface.fill((0,0,90,255))
		
		for object in all_objects:
			self.surface.blit(object.surface, (object.position.x, object.position.y))
				
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
		

Thread(target=App).start()
time.sleep(0.5)

mixer_music.load('../data/loop.ogg')
mixer_music.play(loops = -1)


for i in range(5):
	f = 120*(i+1)
	for j in range(5):
		q = GameObject()
		q.move(Vector2(f, j*120))


x = Player(app)
x.name = 'player1'
x.set_hitbox_offset(12)

