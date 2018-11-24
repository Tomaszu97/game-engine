from pygame			import	*
from game_object	import	*
from player			import	*

class App:	
	
	#just leave 60
	tick = 20
	clock = Clock()
	objects = []


	def __init__(self):
		self._running = True
		self.display = None
		self.size = self.weight, self.height = 1400, 800
		pygame.init()
		self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
				

	def on_init(self): 
		go = Player(2137)
		go.animation_grid = [4,8]
		go.anim_set_spritesheet('../data/scaled_xbr.png')
		go.display_border = True
		go.display_hitbox = True
		go.display_id = True
		go.movement_speed_vector = Vector2(-1,-2)
		self.objects.append(go)

		on = GameObject(420)
		on.anim_set_spritesheet('../data/konon.png')
		on.display_border = True
		on.display_hitbox = True
		on.display_id = True
		on.movement_speed_vector = Vector2(2,1)
		self.objects.append(on)
	

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False
			

	def on_loop(self):
		for object in self.objects:
			object.every_tick()

		if(self.objects[0].collide(self.objects[1])):
			print("yas bitch")
		else:
			print("no, ni[B][B]a")
		

	def on_render(self):
		self.display.fill((0,0,0,255))
		
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

		