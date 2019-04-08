from game_object import *
from shared import *

class Bullet(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		self.type =	ObjectType.BULLET
		self.name = 'bullet'
		self.animation_grid			=	[1,5]	#always before setting spritesheet
		self.animation_speed		=   4
		self.set_animation_spritesheet('../data/bullet.png')
		self.set_hitbox_offset(12)

		self.mass = 20
		
		#object specific
		self.damage		=	36
		self.speed		=	10
		self.acceleration	=	0
		