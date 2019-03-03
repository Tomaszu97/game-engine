from game_object import *

class Bullet(GameObject):
	def __init__(self, id):
		super().__init__(id)
		self.type =	ObjectType.BULLET

		#object specific
		damage  =   36

		self.anim_set_spritesheet('../data/bullet.png')