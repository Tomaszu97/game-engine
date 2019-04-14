from game_object import *
from player import *
from shared import *

#TODO - do spawning instead of moving

class Spawner(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0), spawn_object  = None, schedule_period=  1000):
		super().__init__(parent, position)
		
		self.type =	ObjectType.SPAWNER
		self.name = 'spawner'
		self.set_animation_spritesheet('../data/spawner.png')
		self.layer = 10

		#object specific
		self.clock				=	Clock()
		self.counter			=	0
		self.spawn_object		=	spawn_object
		self.schedule_period	=	schedule_period
		self.schedule_once		=	False
		self.running			=	False
		

	def start(self):
		self.counter = 0
		self.running = True

	def stop(self):
		self.running = False


	def every_tick(self):
		super().every_tick()
		self.clock.tick()

		if not self.running:
			return

		self.counter += self.clock.get_time()
		if self.counter > self.schedule_period:
			
			
			#TODO - pass object before and spawn its copy in this place
			x = Bullet()
			x.move(self.position+(self.size/2)-(x.size/2))
			x.movement_speed = Vector2(0,x.speed)

			self.counter = 0
			if self.schedule_once:
				self.stop()

