from pygame import *
from pygame.locals import *
from game_object import *
from player import *

class App:	
	
	#just leave 120
	tick = 120
	clock = Clock()
	objects = []


	def __init__(self):
		self._running = True
		self.display = None
		self.size = self.weight, self.height = 720, 480
		pygame.init()
		self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
				

	def on_init(self): 
		go = Player(2137)
		go.animation_grid = [4,8]
		go.anim_set_spritesheet('../data/scaled_xbr.png')
		self.objects.append(go)

		on = GameObject(420)
		on.anim_set_spritesheet('../data/konon.png')
		on.movement_speed_vector = Vector2(2,1)
		self.objects.append(on)
	

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False
			

	def on_loop(self):
		for object in self.objects:
			object.every_tick()
		

	def on_render(self):
		self.display.fill((0,255,0,255))
		
		for object in self.objects:
			self.display.blit(object.surface, (object.rect.left, object.rect.top))
			
		pygame.display.flip()
		

	def on_cleanup(self):
		pygame.quit()
 

	def on_execute(self):
		if self.on_init() == False:
			self._running = False
 
		while( self._running ):
			for event in pygame.event.get():
				self.on_event(event)
			
			self.on_loop()
			self.clock.tick(self.tick)
			self.on_render()
		
		self.on_cleanup()
		

	def spawn(self, object_type = ObjectType.NULL):
		pass

		