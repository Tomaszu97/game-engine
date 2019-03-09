from game_object import *
from shared import *

class Spawner(GameObject):
	def __init__(self, id):
		super().__init__(id)
		self.type =	ObjectType.SPAWNER

		#object specific
		self.schedule_periods	=	[]
		self.schedule_once		=	[]

		#dd
		self.anim_set_spritesheet('../data/spawner.png')