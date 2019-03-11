from game_object import *
from shared import *

class Spawner(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		self.type =	ObjectType.SPAWNER
		self.name = 'spawner'

		#object specific
		self.schedule_periods	=	[]
		self.schedule_once		=	[]

		#dd
		self.set_animation_spritesheet('../data/spawner.png')