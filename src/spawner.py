from game_object import *

class Player(GameObject):
	def __init__(self, id):
		super().__init__(id)
		self.type =	ObjectType.SPAWNER

		#object specific
		self.schedule_periods	=	[]
		self.schedule_once		=	[]