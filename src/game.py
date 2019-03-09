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
		self.children = []
		global app
		app = self

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
		for object in all_objects:
			object.every_tick()
			for other_object in all_objects:
				if object is not other_object:
					object.collide(other_object)
			
			#kill object if out of bounds
			w, h = pygame.display.get_surface().get_size()
			if not ( object.rect.left in range(-object.rect.width, w) and object.rect.top in range(-object.rect.height, h) ):
				object.kill()


			

	def render(self):
		self.surface.fill((0,0,90,255))
		
		for object in all_objects:
			self.surface.blit(object.surface, (object.rect.left, object.rect.top))
				

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

mixer_music.load('../data/kirbys_theme.mp3')
#mixer_music.play()



for i in range(5):
	f = 120*(i+1)
	for j in range(5):
		q = GameObject()
		q.move(f, j*120)


x = Player(app)
x.name = 'player1'
x.set_hitbox_offset(12)

