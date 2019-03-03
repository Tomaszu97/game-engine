from enum			import	Enum
from math			import	floor, ceil
from pygame			import	*
from pygame.time	import	*
from pygame.key		import	*
from pygame.sprite	import	*
from pygame.surface import	*
from pygame.font	import	*


class ObjectType(Enum):
	NULL	=	0
	PLAYER	=	1
	ALLY	=	2
	ENEMY	=	3
	SPAWNER	=	4
	BULLET	=	5

	
class GameObject(Sprite):
	def __init__(self, parent):
		super().__init__()	

		#identity related
		self.name			=	'object'
		self.type			=	ObjectType.NULL
		self.parent = parent
		self.children	=	[]
		
		#look related
		self.display_border		=	False
		self.display_hitbox		=	False
		self.display_name		=	False
		self.surface			=	Surface((0,0), pygame.SRCALPHA, 32)
		self.font				=	Font('../data/3 Minecraft-Bold.otf', 14 )
		self.name_surface			=	self.font.render( self.name, False, Color(0,255,0,255), Color(0,0,255,80) )

		#position related
		self.rotation			=	0
		self.rect				=	Rect((0,0),(0,0))
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

		self.parent.children.append(self)
		
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
			if self.display_hitbox:
   				draw.rect(self.surface, Color(255,0,0,255), Rect(10, 10, self.hitbox.width, self.hitbox.height), 1)
			if self.display_border:
				draw.rect(self.surface, Color(255,255,0,255), Rect(0,0,self.rect.width, self.rect.height), 1)
			if self.display_name:
				self.surface.blit(self.name_surface, (0,0))

				

		##call scheduled functions

		##move
		self.movement_speed_vector += self.movement_acceleration
		self.move(self.movement_speed_vector.x, self.movement_speed_vector.y)
		
		
	def schedule(self, period, once=False):
		print('object scheduled method')
	
	
	def collide(self, other_object):
		# #calculate relative position
		xdif = (other_object.hitbox.left + (other_object.hitbox.width/2) - (self.hitbox.left + (self.hitbox.width/2)) ) #positive means other_game_object is right to self
		ydif = (other_object.hitbox.top + (other_object.hitbox.height/2) - (self.hitbox.top + (self.hitbox.height/2)) )	#positive means other_game_object is down to self
		#simple sign function
		sign = lambda number : 1 if number > 0 else (-1 if number < 0 else(0) )

		#self left-top point
		lt = (self.hitbox.left, self.hitbox.top)
		#self right-top point
		rt = (self.hitbox.right, self.hitbox.top)
		#self left-bottom point
		lb = (self.hitbox.left, self.hitbox.bottom)
		#self right-bottom point
		rb = (self.hitbox.right, self.hitbox.bottom)
		
		##optimize it for sure
		# ##self approaching other from:
		# if self.id == 36:
		# 	#left
		# 	if not other_object.hitbox.collidepoint(lt) and other_object.hitbox.collidepoint(rt) and other_object.hitbox.collidepoint(rb) and not other_object.hitbox.collidepoint(lb):
		# 		print('l')
		# 	#left upper
		# 	if not other_object.hitbox.collidepoint(lt) and not other_object.hitbox.collidepoint(rt) and other_object.hitbox.collidepoint(rb) and not other_object.hitbox.collidepoint(lb):
		# 		print('lu')
		# 	#up
		# 	if not other_object.hitbox.collidepoint(lt) and not other_object.hitbox.collidepoint(rt) and other_object.hitbox.collidepoint(rb) and other_object.hitbox.collidepoint(lb):
		# 		print('u')
		# 	#right upper
		# 	if not other_object.hitbox.collidepoint(lt) and not other_object.hitbox.collidepoint(rt) and not other_object.hitbox.collidepoint(rb) and other_object.hitbox.collidepoint(lb):
		# 		print('ru')
		# 	#right
		# 	if other_object.hitbox.collidepoint(lt) and not other_object.hitbox.collidepoint(rt) and not other_object.hitbox.collidepoint(rb) and other_object.hitbox.collidepoint(lb):
		# 		print('r')
		# 	#right bottom
		# 	if other_object.hitbox.collidepoint(lt) and not other_object.hitbox.collidepoint(rt) and not other_object.hitbox.collidepoint(rb) and not other_object.hitbox.collidepoint(lb):
		# 		print('rb')
		# 	#bottom
		# 	if other_object.hitbox.collidepoint(lt) and other_object.hitbox.collidepoint(rt) and not other_object.hitbox.collidepoint(rb) and not other_object.hitbox.collidepoint(lb):
		# 		print('b')
		# 	#left bottom
		# 	if not other_object.hitbox.collidepoint(lt) and other_object.hitbox.collidepoint(rt) and not  other_object.hitbox.collidepoint(rb) and not other_object.hitbox.collidepoint(lb):
		# 		print('lb')
		# 	#is inside
		# 	if other_object.hitbox.collidepoint(lt) and other_object.hitbox.collidepoint(rt) and other_object.hitbox.collidepoint(rb) and other_object.hitbox.collidepoint(lb):
		# 		print('i')


		# #calculate elastic collision
		# vel_x_before = self.movement_speed_vector.x
		# vel_y_before = self.movement_speed_vector.y
		# other_vel_x_before = other_object.movement_speed_vector.x
		# other_vel_y_before = other_object.movement_speed_vector.y
		# vel_x = floor( abs( ( vel_x_before*(self.mass-other_object.mass) + 2*other_object.mass*other_vel_x_before )  / (self.mass + other_object.mass) ) )
		# vel_y = floor( abs( ( vel_y_before*(self.mass-other_object.mass) + 2*other_object.mass*other_vel_y_before )  / (self.mass + other_object.mass) ) )
		# other_vel_x = floor( abs( ( other_vel_x_before*(other_object.mass - self.mass) + 2*self.mass*vel_x_before )  / (self.mass + other_object.mass) ) )
		# other_vel_y = floor( abs( ( other_vel_y_before*(other_object.mass - self.mass) + 2*self.mass*vel_y_before )  / (self.mass + other_object.mass) ) )
	

	def set_rect(self, rect):
		self.rect			=	rect

		self.hitbox.width	=	self.rect.width - 20
		self.hitbox.height	=	self.rect.height - 20
		self.hitbox.left	=	10 + self.rect.left
		self.hitbox.top		=	10 + self.rect.top
		
		self.surface	=	Surface((rect.width, rect.height), pygame.SRCALPHA, 32)
	

	def anim_set_spritesheet(self, spritesheet):
		self.animation_spritesheet	=	pygame.image.load(spritesheet).convert_alpha()
		

		temp_rect = Rect(0,0,0,0)
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