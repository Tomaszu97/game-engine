from game_object import *
from shared import *

class Decoration(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		self.type =	ObjectType.DECORATION
		self.name = 'decor'
		self.layer = collision_layer - 1
		self.animation_grid			=	[1,1]	#always before setting spritesheet
		self.set_animation_spritesheet('../data/decoration.png')
		self.mass = 0

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
