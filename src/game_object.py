import sys
from enum import Enum
from math import floor
from pygame import *
from pygame.locals import *
from pygame.time import *
from pygame.key import *
from pygame.sprite import *
from pygame.surface import *


class ObjectType(Enum):
	NULL	=	0
	PLAYER	=	1
	ALLY	=	2
	ENEMY	=	3
	SPAWNER	=	4
	BULLET	=	5
	
class GameObject(Sprite):
	
	def __init__(self, id):
		super().__init__()	

		#identity related
		self.name			=	'game_object'
		self.id				=	id
		self.type			=	ObjectType.NULL
		self.children_ids	=	[]
		
		#look related
		self.display_border		=	False
		self.display_hitbox		=	False
		self.display_id			=	False
		self.surface			=	Surface((0,0), pygame.SRCALPHA, 32)
		
		#position related
		self.rotation			=	0
		self.rect				=	Rect((0,0),(0,0))
		self.hitbox				=	Rect((0,0),(0,0))

		#movement related - OK
		self.movement_speed_vector		=	Vector2(0,0)
		self.movement_acceleration		=	Vector2(0,0)
		self.movement_rotation_speed	=	0
		
		#animation related - OK
		self.animation_spritesheet	=	Surface((0,0), pygame.SRCALPHA, 32)
		self.animation_grid			=	[1,1]	#frames,tracks
		self.animation_speed		=	4		#ticks per frame
		self.animation_frame		=	0
		self.animation_track		=	0
		self.animation_counter		=	0
		self.animation_paused		=	False
		
		#behavior
		self.mass				=	36
		self.physical			=	False	#physical=False forces transparent collisions
		
	def move(self, x=0, y=0):
		self.rect.top		+=	y
		self.rect.left		+=	x 
		self.hitbox.top		+=	y
		self.hitbox.left	+=	x


	def on_create(self):
		print('created object')
		##generate id
		

	def on_destroy(self):
		print('destroyed object')
		##what to do with children?


	def every_tick(self):
		##animate		
		self.animation_counter += 1
		if(self.animation_counter >= self.animation_speed):
			self.animation_counter = 0
			#every frame
			if not self.animation_paused:
				self.animation_frame += 1
				if(self.animation_frame >= self.animation_grid[1]):
					self.animation_frame = 0;
			#redraw spritesheet to self.surface (+ optional hitbox + optional border)
			self.surface.fill((0,0,0,0))
			self.surface.blit(self.animation_spritesheet, (0,0), Rect(self.rect.width*self.animation_frame, self.rect.height*self.animation_track, self.rect.width,self.rect.height))
			if self.display_hitbox:
   				draw.rect(self.surface, Color(255,0,0,255), Rect(0.1*self.rect.width,0.1*self.rect.height, self.hitbox.width, self.hitbox.height), 1)
			if self.display_border:
				draw.rect(self.surface, Color(0,255,0,255), Rect(0,0,self.rect.width, self.rect.height), 1)
			

		##call scheduled functions

		##move
		self.movement_speed_vector += self.movement_acceleration
		self.move(self.movement_speed_vector.x, self.movement_speed_vector.y)
		
		
	def schedule(self, period, once=False):
		print('object scheduled method')
	
	
	def collide(self, other_game_object):
		print(self.hitbox)
		print(other_game_object.hitbox)
		return self.hitbox.colliderect(other_game_object.hitbox)
	

	def spawn_child(self):
		print('spawned a child')
		pass
	
	
	def anim_set_spritesheet(self, spritesheet):
		self.animation_spritesheet	=	pygame.image.load(spritesheet).convert_alpha()
		
		self.rect.width		=	floor(self.animation_spritesheet.get_rect().width/self.animation_grid[1])
		self.rect.height	=	floor(self.animation_spritesheet.get_rect().height/self.animation_grid[0])
		self.hitbox.width	=	0.8 * self.rect.width
		self.hitbox.height	=	0.8 * self.rect.height
		self.hitbox.left	=	0.1 * self.rect.width
		self.hitbox.top		=	0.1 * self.rect.height
	
		self.surface	=	Surface((self.rect.width, self.rect.height), pygame.SRCALPHA, 32)


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