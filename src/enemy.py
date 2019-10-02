from game_object    import *
from bullet         import *
from shared         import *

class EnemyType(Enum):
	NULL        = 0
	WANDERING   = 1
	FOLLOWING   = 2
	STATIONERY  = 3
	ORBITING    = 4
	ESCAPING    = 5 


class Enemy(GameObject):
	def __init__(self, parent=None, position=Vector2(0.0, 0.0), target_list=None):
		super().__init__(parent, position)

		self.type = ObjectType.ENEMY

		self.target_list = target_list
		self.target = self.choose_target()

		#object specific
		self.hp = 100
		self.speed = 1
		self.sight_radius = 400
		self.damage = 5

		#state related        
		self.state_clock        = Clock()           # clock to measure time in states
		self.state_timer        = 0                 # time in actual state
		self.idle_to_patrol     = 4000              # when to start patroling
		self.waypoint           = None              # waypoint used in patroling
		self.state              = self.idle         # current state of enemy
		self.attack_range       = 300
		self.attack_state       = None
		self.attack_list        = []
		self.cooldown_time      = 0                 # time from one skill to another

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
									'PLAYER'	:	['bounce'],
									'ALLY'		:	[],
									'ENEMY'		:	[],
									'SPAWNER'	:	[],
									'BULLET'	:	['take_damage'],
									'CONTAINER'	:	[],
									'DECORATION':	[],
									'LABEL'		:	[],
									'WALL'		:	['bounce']}

		self.team = False

	def check_collideable(self, object):
		if object.type.name == 'BULLET':
			if object.team == self.team:
				return False
		return self.is_collideable[str(object.type.name)]

	def every_tick(self):
		self.state_clock.tick()
		self.state_timer += self.state_clock.get_time()
		self.state()
		return super().every_tick()

	def choose_target(self):
		if self.target_list:
			return(random.choice(self.target_list))
		return None

	##################### STATES ##########################
	#TODO: Add attack state

	# just standing still, after a while -> patrolling
	def idle(self):
		self.movement_speed = Vector2(0.0, 0.0)
		distance = Vector2(self.target.position - self.position).length()
		if distance < self.sight_radius:
			self.state_timer = 0
			self.state = self.follow        
		if self.state_timer > self.idle_to_patrol:
			self.state_timer = 0
			self.choose_waypoint()
			self.state = self.patrol
			
	# following a target if in sight range
	def follow(self):
		direction = Vector2(self.target.position - self.position)
		distance = direction.length()
		direction = direction.normalize()
		self.movement_speed = direction * self.speed
		if distance < self.attack_range:
			if self.cooldown_time < self.state_timer:
				self.state_timer = 0
				self.attack_state = self.choose_skill
				self.state = self.attack
		elif distance > self.sight_radius:
			self.state_timer = 0
			self.state = self.idle
	
	# walking to a random waypoint
	def patrol(self):
		distance = Vector2(self.target.position - self.position).length()
		waypoint_dist = Vector2(self.waypoint - self.position)
		if distance < self.sight_radius:
			self.state_timer = 0
			self.state = self.follow
		elif waypoint_dist.length() < 50:            
			self.state_timer = 0
			self.state = self.idle 
		elif self.state_timer > 5000:  
			self.state_timer = 0
			self.state = self.idle     
		waypoint_dist = waypoint_dist.normalize()
		self.movement_speed = waypoint_dist * self.speed  

	# choosing a waypoint
	def choose_waypoint(self):
		self.waypoint = (Vector2((random.randint(0,window_size[1]), random.randint(0, window_size[0]))))  

	def attack(self):
		self.attack_state()

	def choose_skill(self):
		self.attack_state = random.choice(self.attack_list)
			
	##################### SKILLS ##########################
	# TODO: Add choose_skill, cooldown

	def charging(self, charge_time):
		pass

	# boosts speed for few seconds
	def speed_boost(self):
		boost_multiplier = 3
		distance = Vector2(self.target.position - self.position)
		distance = distance.normalize()
		self.movement_speed = distance * self.speed * boost_multiplier
		if self.state_timer > 2000:
			self.state_timer = 0
			self.attack_state = self.exhausted

	# shoots a bullet every 'cooldown_time' seconds
	def shoot(self):
		bullet = Bullet(self)
		bullet.move( (self.position+(self.size/2) - bullet.size/2))

		shooting_direction = Vector2(self.target.position) -  (self.position)
		shooting_direction = shooting_direction.normalize()
		try:
			bullet.movement_speed = shooting_direction * bullet.speed * 0.5
			q = Vector2()
			q.from_polar(( self.hitbox_size.length()/2 + bullet.hitbox_size.length()/2,  shooting_direction.as_polar()[1]))
			bullet.move(q)
		except ValueError:
			bullet.kill()

		self.cooldown_time = 3000
		self.state_timer = 0
		self.state = self.idle

	def teleport(self):
		new_position = (Vector2((random.randint(0,window_size[1]), random.randint(0, window_size[0])))) 
		
	def cooldown(self):
		pass

	def exhausted(self):
		exhaust_lenght = 3000
		self.movement_speed *= 0.999
		if self.state_timer > exhaust_lenght:
			self.state_timer = 0
			self.state = self.idle 

	# def bounce(self, other_object):
	# 	sign = lambda x: 1 if x>=0 else -1

	# 	#return if object width or height is 0
	# 	if other_object.hitbox_size.x == 0 or other_object.hitbox_size.y == 0:
	# 		return


	# 	#move them away and collide
	# 	if Rect(self.hitbox_position, self.hitbox_size).colliderect(Rect(other_object.hitbox_position, other_object.hitbox_size)):
	# 		relative_position = self.position + (self.size/2) - other_object.position - (other_object.size/2)
	# 		total_speed = self.movement_speed + other_object.movement_speed

	# 		if self.mass == 0 or other_object.mass == 0:
	# 			mass_ratio = 1
	# 			other_mass_ratio = 1
	# 		else:
	# 			mass_ratio = self.mass / (self.mass+other_object.mass)
	# 			other_mass_ratio = other_object.mass / (self.mass+other_object.mass)	


	# 		#relpos from other to me
	# 		if relative_position.x < 0:
	# 			#self approach from the left
	# 			x_intersection = -round(self.hitbox_position.x+self.hitbox_size.x-other_object.hitbox_position.x)
	# 		else:
	# 			#self approach from the right
	# 			x_intersection = round(other_object.hitbox_position.x+other_object.hitbox_size.x-self.hitbox_position.x)
	# 		if relative_position.y < 0:
	# 			#self approach from above
	# 			y_intersection = -round(self.hitbox_position.y+self.hitbox_size.y-other_object.hitbox_position.y)
	# 		else:
	# 			#self approach from below
	# 			y_intersection = round(other_object.hitbox_position.y+other_object.hitbox_size.y-self.hitbox_position.y)
			
	# 		if abs(x_intersection) > abs(y_intersection):
	# 			if self.mass != 0:
	# 				self.move(0, y_intersection*other_mass_ratio)
	# 				self.movement_speed.y = sign(y_intersection)*abs(other_mass_ratio*total_speed.y)
	# 			if other_object.mass != 0:
	# 				other_object.move(0, -y_intersection*mass_ratio)
	# 				other_object.movement_speed.y = -sign(y_intersection)*abs(mass_ratio*total_speed.y)
	# 		else:
	# 			if self.mass != 0:
	# 				self.move(x_intersection*other_mass_ratio, 0)
	# 				self.movement_speed.x = sign(x_intersection)*abs(other_mass_ratio*total_speed.x)
	# 			if other_object.mass != 0:
	# 				other_object.move(-x_intersection*mass_ratio, 0)
	# 				other_object.movement_speed.x = -sign(x_intersection)*abs(mass_ratio*total_speed.x)

	# 		if other_object.friendly_m:
	# 			if isinstance(other_object, Bullet):
	# 				self.hp -= other_object.damage
	# 				other_object.kill()

	# 		if self.hp <= 0:
	# 			exp = Explosion(parent=None ,position=(self.position - self.size/2))
	# 			self.kill()		


class Enemy_Following(Enemy):
	def __init__(self, parent=None, position=Vector2(0.0, 0.0), target_list=None):
		super().__init__(parent, position, target_list)
		self.enemy_type = EnemyType.FOLLOWING
		self.set_animation_spritesheet('../data/konon.png')
		self.animation_speed = 0.25
		self.mass = 1000
		self.attack_list = [self.speed_boost]

	def every_tick(self):
		return super().every_tick()

class Enemy_Orbiting(Enemy):
	def __init__(self, parent=None, position=Vector2(0.0, 0.0), target_list=None):
		super().__init__(parent, position, target_list)

		self.enemy_type = EnemyType.ORBITING
		self.animation_grid = [2,2]
		self.set_animation_spritesheet('../data/konon2.png')
		self.mass = 1000
		self.attack_list = [self.shoot]

	# overwritten follow to orbit around player
	def follow(self):
		distance = Vector2(self.target.position - self.position)
		if distance.length() > self.sight_radius:
			self.state_timer = 0
			self.state = self.idle
		distance = distance.normalize()
		distance = distance.rotate(90)   
		self.movement_speed = distance * self.speed
		if distance.length() < self.sight_radius:
			if self.cooldown_time < self.state_timer:
				self.state_timer = 0
				self.attack_state = self.choose_skill
				self.state = self.attack

	def every_tick(self):
		return super().every_tick()

class Enemy_Wandering(Enemy):
	def __init__(self, parent=None, position=Vector2(0.0, 0.0), target_list=None):
		super().__init__(parent, position, target_list)

		self.enemy_type = EnemyType.WANDERING
		
		self.set_animation_spritesheet('../data/konon.png')
		self.mass = 1000
		self.idle_to_patrol = 500

	def idle(self):
		self.movement_speed = Vector2(0.0, 0.0)      
		distance = Vector2(self.target.position - self.position)  
		if self.state_timer > self.idle_to_patrol:
			self.state_timer = 0
			self.state = self.choose_waypoint
		
	def patrol(self):
		distance = Vector2(self.target.position - self.position)
		waypoint_dist = Vector2(self.waypoint - self.position)

		if waypoint_dist.length() < 50:            
			self.state_timer = 0
			self.state = self.idle 
		elif self.state_timer > 5000:  
			self.state_timer = 0
			self.state = self.idle     
			
		waypoint_dist = waypoint_dist.normalize()
		self.movement_speed = waypoint_dist * self.speed  

	def every_tick(self):
		return super().every_tick()
