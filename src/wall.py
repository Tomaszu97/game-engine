from game_object import *
from shared import *

class Wall(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		self.type =	ObjectType.WALL
		self.name = 'wall'
		self.layer = collision_layer
		self.animation_grid			=	[1,1]	#always before setting spritesheet
		self.set_animation_spritesheet('../data/smallwall.png')
		self.mass = 0
		self.is_collideable		=  {'NULL' 		:	True,
									'PLAYER'	:	True,
									'ALLY'		:	True,
									'ENEMY'		:	True,
									'SPAWNER'	:	True,
									'BULLET'	:	True,
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
