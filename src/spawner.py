from bullet			import *
from decoration		import *
from enemy			import *
from game_object	import *
from label			import *
from player			import *
from shared			import *
from trapdoor		import *
from wall			import *


class Spawner(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0), spawn_object = None, schedule_period=  1000):
		super().__init__(parent, position)
		
		self.type =	ObjectType.SPAWNER
		self.name = 'spawner'
		self.set_animation_spritesheet('../data/spawner.png')
		self.layer = collision_layer + 1
		self.mass = 0

		#object specific
		self.clock				=	Clock()
		self.counter			=	0
		self.spawn_object		=	spawn_object
		self.schedule_period	=	schedule_period
		self.schedule_once		=	False
		self.running			=	False

		self.is_collideable		=  {'NULL' 		:	False,
									'PLAYER'	:	False,
									'ALLY'		:	False,
									'ENEMY'		:	False,
									'SPAWNER'	:	False,
									'BULLET'	:	False,
									'CONTAINER'	:	False,
									'DECORATION':	False,
									'LABEL'		:	False,
									'WALL'		:	False}
								
		self.proccess_collision = {	'NULL' 		:	[],
									'PLAYER'	:	[],
									'ALLY'		:	[],
									'ENEMY'		:	[],
									'SPAWNER'	:	[],
									'BULLET'	:	[],
									'CONTAINER'	:	[],
									'DECORATION':	[],
									'LABEL'		:	[],
									'WALL'		:	[]}

		

	def start(self):
		self.counter = 0
		self.running = True

	def stop(self):
		self.running = False


	def every_tick(self):
		self.clock.tick()
		if self.running:
			self.counter += self.clock.get_time()
			if self.counter > self.schedule_period:
				
				
				#TODO - pass object before and spawn its copy in this place
				x = Bullet()
				x.move(self.position+(self.size/2)-(x.size/2))
				x.movement_speed = Vector2(0,x.speed)

				self.counter = 0
				if self.schedule_once:
					self.stop()
		
		return super().every_tick()

