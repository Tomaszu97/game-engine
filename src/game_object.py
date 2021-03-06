from enum			import	Enum
from pygame			import	*
from pygame.time	import	*
from pygame.key		import	*
from pygame.sprite	import	*
from pygame.surface import	*
from pygame.font	import	*
from shared 		import	*
import	copy


class ObjectType(Enum):
	NULL		=	0
	PLAYER		=	1
	ALLY		=	2
	ENEMY		=	3
	SPAWNER		=	4
	BULLET		=	5
	CONTAINER	=	6
	DECORATION	=	7
	LABEL		=	8
	WALL		=	9
	TRAPDOOR	=	10
	DIALOG		=	11

	
class GameObject(Sprite):
	#set default values, handlers, textures etc.
	def __init__(self, parent=None, position = Vector2(0.0, 0.0)):
		super().__init__()

		#identity related
		self.name			=	'object'
		self.type			=	ObjectType.NULL
		self.parent 		= 	parent
		self.children		=	[]
		
		#look related
		self.surface			=	Surface((0,0), pygame.SRCALPHA, 32)
		self.font				=	Font('../data/1 Minecraft-Regular.otf', 10 )

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
		self.animation_grid			=	[1,1]	#tracks, frames
		self.animation_speed		=	4		#ticks per frame
		self.animation_frame		=	0
		self.animation_track		=	0
		self.animation_counter		=	0
		self.animation_paused		=	False
		
		#collision behavior
		self.mass				=	1000
		self.layer				=	collision_layer
		self.team 				= 	None		# for bullets (team None - neutral, True - friendly, False - enemy)
		self.to_kill 			= 	False		# marked to kill		
		self.is_invincible		= 	False		# can't be hit

		#which collisions to check
		self.is_collideable		= { ObjectType.NULL 		:	True,
									ObjectType.PLAYER		:	True,
									ObjectType.ALLY			:	True,
									ObjectType.ENEMY		:	True,
									ObjectType.SPAWNER		:	True,
									ObjectType.BULLET		:	True,
									ObjectType.CONTAINER	:	False,
									ObjectType.DECORATION	:	False,
									ObjectType.LABEL		:	False,
									ObjectType.WALL			:	True,
									ObjectType.TRAPDOOR		:	False,
									ObjectType.DIALOG		:	False}
									
		#how to handle collisions with certain objects
		#remember about symmetry if A to B handlers must match B to A handlers		
		self.process_collision	= { ObjectType.NULL 		:	[self.bounce],
									ObjectType.PLAYER		:	[self.bounce],
									ObjectType.ALLY			:	[self.bounce],
									ObjectType.ENEMY		:	[self.bounce],
									ObjectType.SPAWNER		:	[],
									ObjectType.BULLET		:	[self.bounce],
									ObjectType.CONTAINER	:	[self.bounce],
									ObjectType.DECORATION	:	[],
									ObjectType.LABEL		:	[],
									ObjectType.WALL			:	[self.bounce],
									ObjectType.TRAPDOOR		:	[],
									ObjectType.DIALOG		:	[]}

		#append object to children list and all object list
		if self.parent != None:
			self.parent.children.append(self)
		all_objects.append(self)

		#initial look
		self.set_animation_spritesheet(resources.smallcrate)

		#flag for multithreading
		self.ready = True

	#move object on main surface
	def move(self, firstarg=None, secondarg=None):
		if secondarg == None:
			self.position += firstarg
		else:
			self.position += Vector2(firstarg, secondarg)
		
		self.hitbox_position = self.position + Vector2(self.hitbox_offset, self.hitbox_offset)
			
	#update animation, position, speed, acceleration
	def every_tick(self):
		try:
			self.ready
		except:
			return

		#animate		
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
			if display_velocity:
				draw.line(self.surface, Color(0,0,255,255), self.size/2, (self.size/2)+self.movement_speed, 1) 

		#accelrate, break a bit and move
		self.movement_speed += self.movement_acceleration
		self.movement_speed *= slowdown_factor
		self.move(self.movement_speed)
		
	#constrain value in between range
	def constrain(self,val, min_val, max_val):
		return min(max_val, max(min_val, val))
	
	#COLLISIONS#

	#return true if is collideable with object
	def check_collideable(self, object):
		return self.is_collideable[object.type]

	#TODO - handle invincibility
	#return the list of collision handlers
	def get_on_collide(self, object):
		# if self.is_invincible:
		# 	self.process_collision[str(object.type.name)][:-1]
		return self.process_collision[object.type]

	#move object so they don't collide anymore
	def bounce(self, object, other_object):
		sign = lambda x: 1 if x>=0 else -1

		#return if object width or height is 0
		if other_object.hitbox_size.x == 0 or other_object.hitbox_size.y == 0:
			return

		#move them away and collide
		if Rect(object.hitbox_position, object.hitbox_size).colliderect(Rect(other_object.hitbox_position, other_object.hitbox_size)):
			relative_position = object.position + (object.size/2) - other_object.position - (other_object.size/2)
			total_speed = object.movement_speed + other_object.movement_speed

			if object.mass == 0 or other_object.mass == 0:
				mass_ratio = 1
				other_mass_ratio = 1
			else:
				mass_ratio = object.mass / (object.mass+other_object.mass)
				other_mass_ratio = other_object.mass / (object.mass+other_object.mass)	


			#relpos from other to me
			if relative_position.x < 0:
				#self approach from the left
				x_intersection = -round(object.hitbox_position.x+object.hitbox_size.x-other_object.hitbox_position.x)
			else:
				#self approach from the right
				x_intersection = round(other_object.hitbox_position.x+other_object.hitbox_size.x-object.hitbox_position.x)
			if relative_position.y < 0:
				#self approach from above
				y_intersection = -round(object.hitbox_position.y+object.hitbox_size.y-other_object.hitbox_position.y)
			else:
				#self approach from below
				y_intersection = round(other_object.hitbox_position.y+other_object.hitbox_size.y-object.hitbox_position.y)
			
			if abs(x_intersection) > abs(y_intersection):
				if object.mass != 0:
					object.move(0, y_intersection*other_mass_ratio)
					object.movement_speed.y = sign(y_intersection)*abs(other_mass_ratio*total_speed.y)
				if other_object.mass != 0:
					other_object.move(0, -y_intersection*mass_ratio)
					other_object.movement_speed.y = -sign(y_intersection)*abs(mass_ratio*total_speed.y)
			else:
				if object.mass != 0:
					object.move(x_intersection*other_mass_ratio, 0)
					object.movement_speed.x = sign(x_intersection)*abs(other_mass_ratio*total_speed.x)
				if other_object.mass != 0:
					other_object.move(-x_intersection*mass_ratio, 0)
					other_object.movement_speed.x = -sign(x_intersection)*abs(mass_ratio*total_speed.x)

	#TODO: upgrade the formula, move to other class
	#substract hp
	def take_damage(self, object, other_object):
		try:
			self.hp -= other_object.damage
			if self.hp < 0:
				self.kill()
		except AttributeError:
			return

	#change collision flag
	def set_collideable(self, object_type, change_to):
		self.is_collideable[object_type] = change_to

	#change collision handler
	def set_collision_process(self, object_type, change_to):
		self.process_collision[object_type] = change_to

	#SIZE AND HITBOX#
	
	#set size of object and update its hitbox
	def set_size(self, size):
		self.size = size
		self.set_hitbox_offset(self.hitbox_offset)

	#set difference between object size and its hitbox
	def set_hitbox_offset(self, offset):
		self.hitbox_offset = offset
		self.hitbox_position = self.position + Vector2(offset, offset)
		self.hitbox_size = self.size - Vector2(2*offset, 2*offset)
	
	#change spritesheet
	def set_animation_spritesheet(self, spritesheet):
		if isinstance(spritesheet, Surface):
			self.animation_spritesheet = spritesheet
		else:
			self.animation_spritesheet	=	pygame.image.load(spritesheet).convert_alpha()
		self.set_size(Vector2(self.animation_spritesheet.get_rect().width/self.animation_grid[1], self.animation_spritesheet.get_rect().height/self.animation_grid[0]))
		self.surface	=	Surface((self.size.x, self.size.y), pygame.SRCALPHA, 32)

	#change animation
	def change_animation_track(self, track_number):
		if track_number < self.animation_grid[0] and track_number >= 0:
			self.animation_track = track_number
	
	#stop animation and go back to first frame
	def animation_stop(self):
		self.animation_paused = True
		self.animation_frame = 0

	#pause animation without going back to first frame
	def animation_pause(self):
		self.animation_paused = True
	
	#resume animation
	def animation_play(self):
		self.animation_paused = False

	#delete object
	def kill(self):
		try:
			if self.parent != None:
				self.parent.children.remove(self)
			all_objects.remove(self)
		except ValueError:
			return

	#TODO - do this
	#returns a copy of this object
	def copy(self):
		copyobj = GameObject()
		for attr in self.__dict__:
			copyattr = getattr(copyobj, attr)
			selfattr = getattr(self, attr)

			if type(getattr(self,attr)).__name__ == 'Font':		#dont copy font
				print('WARNING: fonts arent copied during object copy')
			elif hasattr(getattr(self, attr), 'copy') and callable(getattr(getattr(self, attr), 'copy')):		#if attribute has copy method then use it
				copyattr = selfattr.copy()
			else:	#in other case use deepcopy
				copyattr = copy.deepcopy(selfattr)

		return copyobj


#GLOBAL FUNCTIONS#

#deletes all objects
def killall():
	all_objects.clear()

#TODO - kill console as well
#exits from program
def quit():
	print('\n\n')
	pygame.quit()


		# #collision overwrite
		# self.is_collideable[ObjectType.NULL]			=	False
		# self.is_collideable[ObjectType.PLAYER]			=	True
		# self.is_collideable[ObjectType.ALLY]			=	False
		# self.is_collideable[ObjectType.ENEMY]			=	True
		# self.is_collideable[ObjectType.SPAWNER]			=	False
		# self.is_collideable[ObjectType.BULLET]			=	False
		# self.is_collideable[ObjectType.CONTAINER]		=	False
		# self.is_collideable[ObjectType.DECORATION]		=	False
		# self.is_collideable[ObjectType.LABEL]			=	False
		# self.is_collideable[ObjectType.WALL]			=	True
		# self.is_collideable[ObjectType.TRAPDOOR]		=	False
		# self.is_collideable[ObjectType.DIALOG]			=	False
		
		# self.process_collision[ObjectType.NULL]			=	[]
		# self.process_collision[ObjectType.PLAYER]		=	[self.take_damage]
		# self.process_collision[ObjectType.ALLY]			=	[]
		# self.process_collision[ObjectType.ENEMY]		=	[self.take_damage]
		# self.process_collision[ObjectType.SPAWNER]		=	[]
		# self.process_collision[ObjectType.BULLET]		=	[]
		# self.process_collision[ObjectType.CONTAINER]	=	[]
		# self.process_collision[ObjectType.DECORATION]	=	[]
		# self.process_collision[ObjectType.LABEL]		=	[]
		# self.process_collision[ObjectType.WALL]			=	[]
		# self.process_collision[ObjectType.TRAPDOOR]		=	[]
		# self.process_collision[ObjectType.DIALOG]		=	[]