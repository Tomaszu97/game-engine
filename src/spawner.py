from game_object import *
from player import *
from shared import *

class Spawner(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		
		self.type =	ObjectType.SPAWNER
		self.name = 'spawner'
		self.set_animation_spritesheet('../data/spawner.png')
		self.layer = 10

		#object specific
		self.counter			=	0
		self.schedule_period	=	-1
		self.schedule_once		=	False
		self.clock				=	Clock()


	def every_tick(self):
		self.clock.tick()
		self.counter += self.clock.get_time()
		if self.counter > self.schedule_period and self.schedule_period != -1:
			
			x = Bullet(self)
			x.move(self.position)
			x.movement_speed = Vector2(1,2)

			self.counter = 0
			if self.schedule_once:
				self.schedule_period = -1

		return super().every_tick()
