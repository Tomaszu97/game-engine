from game_object import *
from shared import *

class Bullet(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		self.type =	ObjectType.BULLET
		self.name = 'bullet'
		self.animation_grid			=	[1,5]	#always before setting spritesheet
		self.animation_speed		=   4
		self.set_animation_spritesheet('../data/smallbullet.png')
		self.set_hitbox_offset(1)
		self.layer = collision_layer

		self.mass = 1
		
		#object specific
		self.ttl_clock	=	Clock()
		self.ttl_timer	=	0
		self.ttl		=	2000 #ms
		self.damage		=	36
		self.speed		=	5

		#collision
		self.is_collideable		=  {'NULL' 		:	True,
									'PLAYER'	:	True,
									'ALLY'		:	True,
									'ENEMY'		:	True,
									'SPAWNER'	:	True,
									'BULLET'	:	True,
									'CONTAINER'	:	False,
									'DECORATION':	False,
									'LABEL'		:	False,
									'WALL'		:	True}
								
		self.proccess_collision = {	'NULL' 		:	[],
									'PLAYER'	:	['take_damage'],
									'ALLY'		:	[],
									'ENEMY'		:	['take_damage'],
									'SPAWNER'	:	[],
									'BULLET'	:	[],
									'CONTAINER'	:	[],
									'DECORATION':	[],
									'LABEL'		:	[],
									'WALL'		:	['bounce']}

		self.team = parent.team
	
	def check_collideable(self, object):
		if self.to_kill:
			return False
		if object.type.name == 'BULLET' or object.type.name == 'PLAYER':
			if object.team == self.team:
				return False
		return self.is_collideable[str(object.type.name)]

	def take_damage(self, other_object):
		self.to_kill = True

	def every_tick(self):
		self.ttl_clock.tick()
		self.ttl_timer += self.ttl_clock.get_time()
		
		if self.ttl_timer > self.ttl:
			self.kill()
		return super().every_tick()