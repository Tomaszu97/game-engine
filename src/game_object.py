import sys
import pygame
from enum import Enum
from pygame import *
from pygame.locals import *
from pygame.time import *
from pygame.key import *
from pygame.sprite import *
from pygame.surface import *
from pygame.math import *

class ObjectType(Enum):
	NULL	=	0
	PLAYER	=	1
	ALLY	=	2
	ENEMY	=	3
	SPAWNER	=	4

class CollisionType(Enum):
	DOMINANT	=	0
	SUBMERSIVE	=	1
	TRANSPARENT	=	2
	HALFWAY		=	3
	
class GameObject(Sprite):
	friendly_name		=	'game_object'
	id					=	0
	type				=	ObjectType.NULL
	collision_type		=	CollisionType.TRANSPARENT
	layer				=	0
	#size is overkill just use rect
	size				=	[100,100]
	rect				=	Rect((0,0),(0,0))
	current_speed		=	Vector2(0,0)
	speed				=	400
	acceleration		=	Vector2(0,0)
	rotation			=	0
	rotation_speed		=	0
	
	animation_grid		=	[1,1]	#frames,tracks
	animation_speed		=	4		#ticks per frame
	animation_frame		=	0
	animation_track		=	0
	animation_counter	=	0
	animation_paused	=	False
	
	display_border		=	False
	display_id			=	False
	physical			=	False	#physical=False forces transparent collisions
	schedule_periods	=	[]
	schedule_once		=	[]
	children_ids		=	[]
	spritesheet			=	Surface((0,0), pygame.SRCALPHA, 32)
	surface				=	Surface((0,0), pygame.SRCALPHA, 32)
	
	
	def __init__(self, id):
		Sprite.__init__(self)
		self.id = id
		
	def move(self, x=0, y=0):
		self.rect.x += x
		self.rect.y += y 
		
	def on_create(self):
		print('created object')
		##generate id
		pass
		
	def every_tick(self):
		##animate
		#every tick
		self.animation_counter += 1
		if(self.animation_counter >= self.animation_speed):
			self.animation_counter = 0
			#every frame
			if not self.animation_paused:
				self.animation_frame += 1
				if(self.animation_frame >= self.animation_grid[1]):
					self.animation_frame = 0;
			self.surface.fill((0,0,0,0))
			self.surface.blit(self.spritesheet, (0,0), Rect(self.size[0]*self.animation_frame, self.size[1]*self.animation_track, self.size[0],self.size[1]))
			
		##call scheduled functions
		#move
		self.current_speed += self.acceleration
		self.rect = self.rect.move(self.current_speed)
		##collide
		pass
		
	def on_destroy(self):
		print('destroyed object')
		##what to do with children?
		pass
	
	def schedule(self, period, once=False):
		print('object scheduled method')
		pass
	
	def collide(self, other_game_object, collision_type = CollisionType.DOMINANT):
		pass
	
	def spawn_child(self):
		print('spawned a child')
		pass
	
	
	def anim_set_spritesheet(self, spritesheet):
		self.spritesheet = pygame.image.load(spritesheet).convert_alpha()
		self.size = (self.spritesheet.get_rect().width/self.animation_grid[1], self.spritesheet.get_rect().height/self.animation_grid[0])
		self.surface = Surface((self.size[0], self.size[1]), pygame.SRCALPHA, 32)
		self.surface.fill((0,0,0,0))
		self.surface.blit(self.spritesheet, (0,0), Rect(0,0,self.size[0],self.size[1]))
		
	def anim_change_track(self, track_number):
		if track_number <= self.animation_grid[1] and track_number >= 0:
			self.animation_track = track_number
	
	def anim_stop(self):
		self.animation_paused = True
		self.animation_frame = 0
		
	def anim_pause(self):
		self.animation_paused = True
	
	def anim_play(self):
		self.animation_paused = False
	
	"""speed = 5
	rotation_speed = 0
	movement_vector = [0,0]
	rotation = 0
	type = ObjectType.NULL
	
	def __init__(self, picture):
		Sprite.__init__(self)
		self.image = pygame.image.load(picture).convert_alpha()
		self.rect = self.image.get_rect()
		self.original_image = self.image
	
	def setPosition(self, x, y):
		self.rect.x = x
		self.rect.y = y
	
	def move(self, x, y):
		self.rect.x += x
		self.rect.y += y
		
	def updateMovement(self):
		self.move(self.movement_vector[0], self.movement_vector[1])
		self.rotate(self.rotation_speed)
		
	def isColliding(self, otherObject):
		if(self.rect.colliderect(otherObject.rect)):
			return True
		else:
			return False
			
	def rotate(self, angle):
		self.rotation += angle
		self.image = pygame.transform.rotate(self.original_image, self.rotation)
		self.rect = self.image.get_rect(center=self.rect.center)
"""
	