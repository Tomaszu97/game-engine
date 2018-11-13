import pygame
from pygame import *
from pygame.locals import *
from game_object import *

class App:	
	
	tick = 60
	clock = Clock()
	objects = []

	def __init__(self):
		self._running = True
		self.display = None
		self.size = self.weight, self.height = 720, 480
		pygame.init()
		self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
				
	def on_init(self): 
		go = GameObject(2137)
		go.animation_grid = [4,8]
		go.set_spritesheet('../data/scaled_xbr.png')
		go.current_speed = Vector2(0,0)
		self.objects.append(go)
		on = GameObject(420)
		on.set_spritesheet('../data/konon.png')
		on.current_speed = Vector2(2,1)
		self.objects.append(on)
	
	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False
			
	def on_loop(self):
		for object in self.objects:
			object.every_tick()
		
		##inputs
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_UP]:
			self.objects[0].move(0, -self.objects[0].speed/self.tick)
			self.objects[0].animation_track = 1
			
		if pressed[pygame.K_DOWN]:
			self.objects[0].move(0, self.objects[0].speed/self.tick)
			self.objects[0].animation_track = 0
			
		if pressed[pygame.K_LEFT]:
			self.objects[0].move(-self.objects[0].speed/self.tick, 0)
			self.objects[0].animation_track = 2

		if pressed[pygame.K_RIGHT]:
			self.objects[0].move(self.objects[0].speed/self.tick, 0)
			self.objects[0].animation_track = 3
		
		if pressed[pygame.K_ESCAPE]:
			self.on_cleanup()
		
		
	def on_render(self):
		self.display.fill((0,255,0,255))
		
		for object in self.objects:
		##FIX DIS
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