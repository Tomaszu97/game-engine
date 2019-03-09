from math			import	floor, ceil
from enum			import	Enum
from pygame			import	*
from pygame.time	import	*
from pygame.key		import	*
from pygame.sprite	import	*
from pygame.surface import	*
from pygame.font	import	*
from shared import *



class ObjectType(Enum):
	NULL	=	0
	PLAYER	=	1
	ALLY	=	2
	ENEMY	=	3
	SPAWNER	=	4
	BULLET	=	5

	
class GameObject(Sprite):
	def __init__(self, parent = None, x=0, y=0):
		super().__init__()	

		#identity related
		self.name			=	'object'
		self.type			=	ObjectType.NULL
		self.parent 		= 	parent
		self.children		=	[]
		
		#look related
		self.surface			=	Surface((0,0), pygame.SRCALPHA, 32)
		self.font				=	Font('../data/3 Minecraft-Bold.otf', 14 )

		#position related
		self.rotation			=	0
		self.rect				=	Rect((x,y),(0,0))
		self.hitbox				=	Rect((0,0),(0,0))

		#movement related
		self.movement_speed_vector		=	Vector2(0,0)
		self.movement_acceleration		=	Vector2(0,0)
		self.movement_rotation_speed	=	0
		
		#animation related
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

		#initial
		self.anim_set_spritesheet('../data/crate.png')

		self.display_border = True
		self.display_hitbox = True
		self.display_name = True

		if self.parent != None:
			self.parent.children.append(self)
		all_objects.append(self)
		
	def move(self, x=0, y=0, rotation=0):
		self.rect.top		+=	y
		self.rect.left		+=	x 
		self.hitbox.top		+=	y
		self.hitbox.left	+=	x


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
			if display_hitboxes:
   				draw.rect(self.surface, Color(255,0,0,255), Rect((self.rect.width-self.hitbox.width)/2, (self.rect.height-self.hitbox.height)/2, self.hitbox.width, self.hitbox.height), 1)
			if display_borders:
				draw.rect(self.surface, Color(255,255,0,255), Rect(0,0,self.rect.width, self.rect.height), 1)
			if display_names:
				self.surface.blit(self.font.render( self.name, False, Color(0,255,0,255), Color(0,0,255,80) ), (0,0))

				

		##call scheduled functions

		##move
		self.movement_speed_vector += self.movement_acceleration
		self.move(self.movement_speed_vector.x, self.movement_speed_vector.y)
		
		
	def schedule(self, period, once=False):
		print('object scheduled method')
	
	
	def collide(self, other_object):       
		selfcenter = (self.hitbox.left + self.hitbox.width/2 , self.hitbox.top + self.hitbox.height/2)
		othercenter = (other_object.hitbox.left + other_object.hitbox.width/2, other_object.hitbox.top + other_object.hitbox.height/2)
	   
		#transform to S(0,0)
		selfcenter = (selfcenter[0]-othercenter[0], selfcenter[1]-othercenter[1])
	   
		#linear function transform
		factor = other_object.hitbox.height / other_object.hitbox.width
	   
		#needs optimization
		if self.hitbox.colliderect(other_object.hitbox):
			if selfcenter[1] > selfcenter[0]*factor:
				if selfcenter[1] > -selfcenter[0]*factor:
					self.move(0, (other_object.hitbox.height-self.hitbox.top+other_object.hitbox.top)/2)
					other_object.move(0, -(other_object.hitbox.height-self.hitbox.top+other_object.hitbox.top)/2)
				else:
					self.move(-(self.hitbox.width-other_object.hitbox.left + self.hitbox.left)/2 , 0)
					other_object.move((self.hitbox.width-other_object.hitbox.left + self.hitbox.left)/2, 0)
			else:
				if selfcenter[1] > -selfcenter[0]*factor:
					self.move((other_object.hitbox.width-self.hitbox.left + other_object.hitbox.left)/2 , 0)
					other_object.move(-(other_object.hitbox.width-self.hitbox.left + other_object.hitbox.left)/2, 0)
				else:
					self.move(0, -(self.hitbox.height-other_object.hitbox.top+self.hitbox.top)/2)
					other_object.move(0, (self.hitbox.height-other_object.hitbox.top+self.hitbox.top)/2)
					
	def set_rect(self, rect, hitbox_offset = 0):
		self.rect			=	rect

		self.hitbox.width	=	self.rect.width - 2*hitbox_offset
		self.hitbox.height	=	self.rect.height - 2*hitbox_offset
		self.hitbox.left	=	self.rect.left + hitbox_offset
		self.hitbox.top		=	self.rect.top + hitbox_offset
		
		self.surface	=	Surface((rect.width, rect.height), pygame.SRCALPHA, 32)

	def set_hitbox_offset(self, offset):
		self.set_rect(self.rect, offset)
	

	def anim_set_spritesheet(self, spritesheet):
		self.animation_spritesheet	=	pygame.image.load(spritesheet).convert_alpha()
		

		temp_rect = Rect(self.rect.x,self.rect.y,0,0)
		temp_rect.width		=	floor(self.animation_spritesheet.get_rect().width/self.animation_grid[1])
		temp_rect.height	=	floor(self.animation_spritesheet.get_rect().height/self.animation_grid[0])

		self.set_rect(temp_rect)
	
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

	def kill(self):
		if self.parent != None:
			self.parent.children.remove(self)
		all_objects.remove(self)