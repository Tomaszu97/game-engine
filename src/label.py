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
		self.layer = 20

		
		#object specific
		self.text = 'Sample Text'
		