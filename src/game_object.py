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
	PLAYER		=	1
	ALLY		=	2
	ENEMY		=	3
	SPAWNER		=	4
	BULLET		=	5
	CONTAINER	=	6
	DECORATION	=	7
	LABEL		=	8
	WALL		=	9

	
class GameObject(Sprite):
	def __init__(self, parent=None, position = Vector2(0.0, 0.0)):
		super().__init__()

		#identity related
		self.name			=	'object'
		self.type			=	ObjectType.NULL
		self.parent 		= 	parent
		self.children		=	[]
		
		#look related
		self.surface			=	Surface((0,0), pygame.SRCALPHA, 32)
		self.font				=	Font('../data/3 Minecraft-Bold.otf', 14 )

		#size/position related
		self.rotation			=	0.0
		self.position			=	Vector2(position)
		self.size				=	Vector2(0.0, 0.0)
		self.hitbox_position	=	Vector2(0.0, 0.0)
		self.hitbox_size		=	Vector2(0.0, 0.0)
		self.hitbox_offset		=	0.0

		#movement related
		self.movement_speed				=	Vector2(0,0)
		self.movement_acceleration		=	Vector2(0,0)
		self.movement_angular_speed		=	0.0
		
		#animation related
		self.animation_spritesheet	=	Surface((0,0), pygame.SRCALPHA, 32)
		self.animation_grid			=	(1,1)	#frames,tracks
		self.animation_speed		=	4		#ticks per frame
		self.animation_frame		=	0
		self.animation_track		=	0
		self.animation_counter		=	0
		self.animation_paused		=	False
		
		#collision behavior
		self.mass				=	1000
		self.layer				=	0
		
		#append to lists
		if self.parent != None:
			self.parent.children.append(self)
		all_objects.append(self)

		#initial look
		self.set_animation_spritesheet('../data/crate.png')

		self.ready = True

		
	def move(self, firstarg=None, secondarg=None):
		if secondarg == None:
			self.position += firstarg
		else:
			self.position += Vector2(firstarg, secondarg)
		
		self.hitbox_position = self.position + Vector2(self.hitbox_offset, self.hitbox_offset)
			

	def every_tick(self):
		try:
			self.ready
		except:
			return

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
			self.surface.blit(self.animation_spritesheet, (0,0), Rect(self.size.x*self.animation_frame, self.size.y*self.animation_track, self.size.x, self.size.y))
			
			
			if display_borders:
				draw.rect(self.surface, Color(255,255,0,255), Rect(0,0,self.size.x, self.size.y), 1)
			if display_hitboxes:
   				draw.rect(self.surface, Color(255,0,0,255), Rect(self.hitbox_offset, self.hitbox_offset, self.hitbox_size.x, self.hitbox_size.y) , 1)
			if display_names:
				self.surface.blit(self.font.render( self.name, False, Color(0,255,0,255), Color(0,0,255,80) ), (0,0))

		
		#accelrate, break a bit and move
		self.movement_speed += self.movement_acceleration
		self.movement_speed *= slowdown_factor
		self.move(self.movement_speed)
		

	def constrain(self,val, min_val, max_val):
		return min(max_val, max(min_val, val))


	def collide(self, other_object):
		sign = lambda x: 1 if x>=0 else -1

		#return if object width or height is 0
		if other_object.hitbox_size.x == 0 or other_object.hitbox_size.y == 0:
			return

		#move them away and collide
		if Rect(self.hitbox_position, self.hitbox_size).colliderect(Rect(other_object.hitbox_position, other_object.hitbox_size)):
			relative_position = self.position + (self.size/2) - other_object.position - (other_object.size/2)
			total_speed = self.movement_speed + other_object.movement_speed

			if self.mass == 0 or other_object.mass == 0:
				mass_ratio = 1
				other_mass_ratio = 1
			else:
				mass_ratio = self.mass / (self.mass+other_object.mass)
				other_mass_ratio = other_object.mass / (self.mass+other_object.mass)	


			#relpos from other to me
			if relative_position.x < 0:
				#self approach from the left
				x_intersection = -round(self.hitbox_position.x+self.hitbox_size.x-other_object.hitbox_position.x)
				# if self.mass != 0:
				# 	self.movement_speed.x = -abs(other_mass_ratio*total_speed.x)
				# if other_object.mass != 0:
				# 	other_object.movement_speed.x = abs(mass_ratio*total_speed.x)
			else:
				#self approach from the right
				x_intersection = round(other_object.hitbox_position.x+other_object.hitbox_size.x-self.hitbox_position.x)
				# if self.mass != 0:
				# 	self.movement_speed.x = abs(other_mass_ratio*total_speed.x)
				# if other_object.mass != 0:
				# 	other_object.movement_speed.x = -abs(mass_ratio*total_speed.x)

			if relative_position.y < 0:
				#self approach from above
				y_intersection = -round(self.hitbox_position.y+self.hitbox_size.y-other_object.hitbox_position.y)
				# if self.mass != 0:
				# 	self.movement_speed.y = -abs(other_mass_ratio*total_speed.y)
				# if other_object.mass != 0:
				# 	other_object.movement_speed.y = abs(mass_ratio*total_speed.y)
			else:
				#self approach from below
				y_intersection = round(other_object.hitbox_position.y+other_object.hitbox_size.y-self.hitbox_position.y)
				# if self.mass != 0:
				# 	self.movement_speed.y = abs(other_mass_ratio*total_speed.y)
				# if other_object.mass != 0:
				# 	other_object.movement_speed.y = -abs(mass_ratio*total_speed.y)
			
					
			if abs(x_intersection) > abs(y_intersection):
				if self.mass != 0:
					self.move(0, y_intersection/2)
					self.movement_speed.y = sign(y_intersection)*abs(other_mass_ratio*total_speed.y)
				if other_object.mass != 0:
					other_object.move(0, -y_intersection/2)
					other_object.movement_speed.y = -sign(y_intersection)*abs(mass_ratio*total_speed.y)

			else:
				if self.mass != 0:
					self.move(x_intersection/2, 0)
					self.movement_speed.x = sign(x_intersection)*abs(other_mass_ratio*total_speed.x)
				if other_object.mass != 0:
					other_object.move(-x_intersection/2, 0)
					other_object.movement_speed.x = -sign(x_intersection)*abs(mass_ratio*total_speed.x)


			# if abs(x_intersection) > abs(y_intersection):
			# 	self.move(0, y_intersection*other_mass_ratio)
			# 	other_object.move(0, -y_intersection*mass_ratio)
			# else:
			# 	self.move(x_intersection*other_mass_ratio, 0)
			# 	other_object.move(-x_intersection*mass_ratio, 0)


			# factor = other_object.hitbox_size.y / other_object.hitbox_size.x
			# displacement = Vector2(0.0,0.0)
			# total_speed = self.movement_speed + other_object.movement_speed
			# mass_ratio = self.mass / (self.mass+other_object.mass)
			# other_mass_ratio = other_object.mass / (self.mass+other_object.mass)

			# if relative_position.y > relative_position.x*factor:
			# 	#approach from below
			# 	if relative_position.y > -relative_position.x*factor:
			# 		displacement = Vector2(0, (other_object.hitbox_size.y-self.hitbox_position.y+other_object.hitbox_position.y)/2)
			# 		if self.mass != 0:
			# 			self.movement_speed.y = abs(other_mass_ratio*total_speed.y)
			# 		if other_object.mass != 0:
			# 			other_object.movement_speed.y = -abs(mass_ratio*total_speed.y)
			# 	#from the left hand side
			# 	else:
			# 		displacement = -Vector2((self.hitbox_size.x-other_object.hitbox_position.x+self.hitbox_position.x)/2, 0)
			# 		if self.mass != 0:
			# 			self.movement_speed.x = -abs(other_mass_ratio*total_speed.x)
			# 		if other_object.mass != 0:
			# 			other_object.movement_speed.x = abs(mass_ratio*total_speed.x)
			# else:
			# 	#from the right hand side
			# 	if relative_position.y > -relative_position.x*factor:
			# 		displacement = Vector2((other_object.hitbox_size.x-self.hitbox_position.x + other_object.hitbox_position.x)/2 , 0)
			# 		if self.mass != 0:
			# 			self.movement_speed.x = abs(other_mass_ratio*total_speed.x)
			# 		if other_object.mass != 0:
			# 			other_object.movement_speed.x = -abs(mass_ratio*total_speed.x)
			# 	#from above
			# 	else:
			# 		displacement = -Vector2(0, (self.hitbox_size.y-other_object.hitbox_position.y+self.hitbox_position.y)/2)
			# 		if self.mass != 0:
			# 			self.movement_speed.y = -abs(other_mass_ratio*total_speed.y)
			# 		if other_object.mass != 0:
			# 			other_object.movement_speed.y = abs(mass_ratio*total_speed.y)

			# #move both objects
			# if self.mass != 0:
			# 	self.move(other_mass_ratio*displacement)
			# if other_object.mass != 0:
			# 	other_object.move(-mass_ratio*displacement)
			

			return True

		return False
					

	def set_size(self, size):
		self.size = size
		self.set_hitbox_offset(self.hitbox_offset)


	def set_hitbox_offset(self, offset):
		self.hitbox_offset = offset
		self.hitbox_position = self.position + Vector2(offset, offset)
		self.hitbox_size = self.size - Vector2(2*offset, 2*offset)
	

	def set_animation_spritesheet(self, spritesheet):
		self.animation_spritesheet	=	pygame.image.load(spritesheet).convert_alpha()
		self.set_size(Vector2(self.animation_spritesheet.get_rect().width/self.animation_grid[1], self.animation_spritesheet.get_rect().height/self.animation_grid[0]))
		self.surface	=	Surface((self.size.x, self.size.y), pygame.SRCALPHA, 32)


	def change_animation_track(self, track_number):
		if track_number <= self.animation_grid[1] and track_number >= 0:
			self.animation_track = track_number
	

	def animation_stop(self):
		self.animation_paused = True
		self.animation_frame = 0


	def animation_pause(self):
		self.animation_paused = True
	

	def animation_play(self):
		self.animation_paused = False

	def kill(self):
		if self.parent != None:
			self.parent.children.remove(self)
		all_objects.remove(self)