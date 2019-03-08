from pygame			import	*
from game_object	import	*
from player			import	*
from spawner		import	*
from bullet 		import	*
from threading import Thread
import time

a = None

class App():
	def __init__(self):
		global a
		a = self
		self.children = []

		self.tick = 75
		self.clock = Clock()
		self.running = True
		self.surface = pygame.display.set_mode((1400, 800), pygame.HWSURFACE | pygame.DOUBLEBUF)
		pygame.init()
		
		self.run()


	def handle_events(self, event):
		if event.type == pygame.QUIT:
			self.quit()
			

	def loop(self):
		for object in self.children:
			object.every_tick()
			#shitty collision detection O(n!)
			for other_object in self.children:
				if object is not other_object:
					object.collide(other_object)
			

	def render(self):
		self.surface.fill((120,0,0,255))
		
		for object in self.children:
			self.surface.blit(object.surface, (object.rect.left, object.rect.top))
			for ob in object.children:
				self.surface.blit(ob.surface, (ob.rect.left, ob.rect.left))
			
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
time.sleep(3)

# go = Player(appobj)
# go.mass = 36
# go.animation_grid = [4,8]
# go.anim_set_spritesheet('../data/scaled_xbr.png')
# # go.display_border = True
# go.display_hitbox = True
# go.display_name = True
# go.movement_speed_vector = Vector2(1,2)

#SET SPRITESHEET AFTER ANIM GRID
