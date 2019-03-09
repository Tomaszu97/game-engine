from game_object import *
from shared import *

class Bullet(GameObject):
	def __init__(self, parent = None, x=0, y=0):
		super().__init__(parent, x, y)

		self.type =	ObjectType.BULLET


		self.animation_grid			=	[1,5]	#always before setting spritesheet
		self.animation_speed		=   10
		self.anim_set_spritesheet('../data/bullet.png')
		
		

		#object specific
		damage  =   36
		