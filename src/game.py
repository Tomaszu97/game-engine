from pygame			import	*
from game_object	import	*
from player			import	*

class App:	
	
	#just leave 60
	tick = 60
	clock = Clock()
	objects = []


	def __init__(self):
		self._running = True
		self.display = None
		self.size = self.weight, self.height = 1400, 800
		pygame.init()
		self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
				

	def on_init(self): 
		go = Player(36)
		go.mass = 36
		go.animation_grid = [4,8]
		go.anim_set_spritesheet('../data/scaled_xbr.png')
		go.display_border = True
		go.display_hitbox = True
		go.display_id = True
		#go.movement_speed_vector = Vector2(-1,-2)
		self.objects.append(go)

		bottom_wall = GameObject(400)
		bottom_wall.mass = 369999
		bottom_wall.set_rect(Rect(600,200,400,100))
		bottom_wall.display_border = True
		bottom_wall.display_hitbox = True
		bottom_wall.display_id = True
		self.objects.append(bottom_wall)

		"""
		x = GameObject(59)
		x.mass = 59
		x.anim_set_spritesheet('../data/konon.png')
		x.display_border = True
		x.display_hitbox = True
		x.display_id = True
		x.movement_speed_vector = Vector2(0,0)
		x.move(900,300)
		self.objects.append(x)

		left_wall = GameObject(100)
		left_wall.mass = 369999
		left_wall.set_rect(Rect(0,0,50,800))
		left_wall.display_border = True
		left_wall.display_hitbox = True
		left_wall.display_id = True
		self.objects.append(left_wall)

		right_wall = GameObject(200)
		right_wall.mass = 369999
		right_wall.set_rect(Rect(0,0,1400,50))
		right_wall.display_border = True
		right_wall.display_hitbox = True
		right_wall.display_id = True
		self.objects.append(right_wall)

		top_wall = GameObject(300)
		top_wall.mass = 369999
		top_wall.set_rect(Rect(1350,0,50,800))
		top_wall.display_border = True
		top_wall.display_hitbox = True
		top_wall.display_id = True
		self.objects.append(top_wall)
		"""
		
		

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False
			

	def on_loop(self):
		for object in self.objects:
			object.every_tick()
			#shitty collision detection O(n!)
			for other_object in self.objects:
				if object is not other_object:
					object.collide(other_object)
			

						

		

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

		