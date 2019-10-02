from game_object import *
from shared import *

class Label(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		self.type =	ObjectType.LABEL
		self.name = 'label'
		self.animation_grid			=	[1,1]	#always before setting spritesheet
		self.animation_speed		=   4
		self.set_animation_spritesheet('../data/label.png')
		self.set_hitbox_offset(12)
		self.layer = collision_layer

		
		#object specific
		self.text = 'Sample Text'
		
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
