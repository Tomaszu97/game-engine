from game_object import *
from shared import *

class Wall(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		self.type =	ObjectType.WALL
		self.name = 'wall'
		self.layer = 0
		self.animation_grid			=	[1,1]	#always before setting spritesheet
		self.set_animation_spritesheet('../data/wall.png')
		self.mass = 0
