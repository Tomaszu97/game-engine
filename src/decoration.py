from game_object import *
from shared import *

class Decoration(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		self.type =	ObjectType.DECORATION
		self.name = 'decoration'
		self.layer = -10
		self.animation_grid			=	[1,1]	#always before setting spritesheet
		self.set_animation_spritesheet('../data/decoration.png')
		self.mass = 0.1
