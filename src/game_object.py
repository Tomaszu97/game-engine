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

		self.is_collideable		= { 'NULL' 		:	True,		# collides with
									'PLAYER'	:	True,
									'ALLY'		:	True,
									'ENEMY'		:	True,
									'SPAWNER'	:	True,
									'BULLET'	:	True,
									'CONTAINER'	:	False,
									'DECORATION':	False,
									'LABEL'		:	False,
									'WALL'		:	True}

		
		self.proccess_collision = {	'NULL' 		:	['bounce'],		# what happens after a collision
									'PLAYER'	:	['bounce'],		# insert a function names without brackets
									'ALLY'		:	['bounce'],		# eg. ['bounce', 'take_damage']
									'ENEMY'		:	['bounce'],		# take_damage has to be always the last one
									'SPAWNER'	:	[],
									'BULLET'	:	['bounce'],
									'CONTAINER'	:	['bounce'],
									'DECORATION':	[],
									'LABEL'		:	[],
									'WALL'		:	['bounce']}


		
		#append to lists
		if self.parent != None:
			self.parent.children.append(self)
		all_objects.append(self)

		#initial look
		self.set_animation_spritesheet('../data/smallcrate.png')

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
	
	
	# COLLISION PART

	# return true if is collideable with "object"
	def check_collideable(self, object):
		return self.is_collideable[str(object.type.name)]

	# return the list what happens after a collision
	def get_on_collide(self, object):
		if self.is_invincible:
			self.proccess_collision[str(object.type.name)][:-1]
		return self.proccess_collision[str(object.type.name)]
	
	# TODO: upgrade the formula
	def take_damage(self, other_object):
		try:
			self.hp -= other_object.damage
			if self.hp < 0:
				self.kill()
		except AttributeError:
			return

	# set if the object is collideable with object_type
	def set_collideable(self, object_type, change_to):
		self.is_collideable[object_type] = change_to

	# sets the collision proccess, change_to in a touple or a list 
	def set_collision_proccess(self, object_type, change_to):
		self.proccess_collision[object_type] = change_to

	# SIZE AND HITBOX
	
	def set_size(self, size):
		self.size = size
		self.set_hitbox_offset(self.hitbox_offset)


	def set_hitbox_offset(self, offset):
		self.hitbox_offset = offset
		self.hitbox_position = self.position + Vector2(offset, offset)
		self.hitbox_size = self.size - Vector2(2*offset, 2*offset)
	

	def set_animation_spritesheet(self, spritesheet):
		if isinstance(spritesheet, Surface):
			self.animation_spritesheet = spritesheet
		else:
			self.animation_spritesheet	=	pygame.image.load(spritesheet).convert_alpha()
		self.set_size(Vector2(self.animation_spritesheet.get_rect().width/self.animation_grid[1], self.animation_spritesheet.get_rect().height/self.animation_grid[0]))
		self.surface	=	Surface((self.size.x, self.size.y), pygame.SRCALPHA, 32)


	def change_animation_track(self, track_number):
		if track_number < self.animation_grid[0] and track_number >= 0:
			self.animation_track = track_number
	

	def animation_stop(self):
		self.animation_paused = True
		self.animation_frame = 0


	def animation_pause(self):
		self.animation_paused = True
	

	def animation_play(self):
		self.animation_paused = False

	def kill(self):
		try:
			if self.parent != None:
				self.parent.children.remove(self)
			shared.all_objects.remove(self)
		except ValueError:
			return

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

##global functions
def killall():
	all_objects.clear()

def quit():
	print('\n\n')
	pygame.quit()
