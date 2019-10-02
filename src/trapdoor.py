from game_object import *
from shared import *

class Trapdoor(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		self.type =	ObjectType.TRAPDOOR
		self.name = 'trapdoor'
		self.layer = collision_layer
		self.animation_grid			=	[1,1]	#always before setting spritesheet
		self.set_animation_spritesheet('../data/decoration.png')
		self.mass = 0
