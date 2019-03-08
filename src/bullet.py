from game_object import *

class Bullet(GameObject):
	def __init__(self, parent, x, y):
		super().__init__(parent, x, y)
		self.type =	ObjectType.BULLET
		self.original_surf = self.surface
		self.anim_set_spritesheet('../data/bullet.png')
		self.animation_grid = [1,1]

		self.move(x, y)

		#object specific
		damage  =   36
		
		self.movement_speed_vector = Vector2(0,2)
	
		def every_tick():
			super().every_tick()