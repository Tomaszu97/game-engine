from game_object import *

class Bullet(GameObject):
	def __init__(self, parent):
		super().__init__(parent)
		self.type =	ObjectType.BULLET

		#object specific
		damage  =   36

		self.anim_set_spritesheet('../data/bullet.png')

		self.movement_speed_vector = Vector2(0,2)


		def every_tick():
			super().every_tick()