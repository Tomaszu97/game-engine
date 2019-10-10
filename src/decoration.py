from game_object import *
from shared import *

class Decoration(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		self.type =	ObjectType.DECORATION
		self.name = 'decor'
		self.layer = collision_layer - 1
		self.animation_grid			=	[1,1]	#always before setting spritesheet
		self.set_animation_spritesheet(resources.decoration)
		self.mass = 0

		#collision overwrite
		self.is_collideable[ObjectType.NULL]			=	False
		self.is_collideable[ObjectType.PLAYER]			=	False
		self.is_collideable[ObjectType.ALLY]			=	False
		self.is_collideable[ObjectType.ENEMY]			=	False
		self.is_collideable[ObjectType.SPAWNER]			=	False
		self.is_collideable[ObjectType.BULLET]			=	False
		self.is_collideable[ObjectType.CONTAINER]		=	False
		self.is_collideable[ObjectType.DECORATION]		=	False
		self.is_collideable[ObjectType.LABEL]			=	False
		self.is_collideable[ObjectType.WALL]			=	False
		self.is_collideable[ObjectType.TRAPDOOR]		=	False
		self.is_collideable[ObjectType.DIALOG]			=	False

class ProgressBar(Decoration):
	pass
