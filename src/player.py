from game_object import	*
from wall import	*
from bullet import	*
from shared import	*

class Player(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		self.type =	ObjectType.PLAYER
		self.name = 'player'
		self.animation_grid = [6,4]
		self.set_animation_spritesheet(resources.smallcoloredplayer)
		self.mass = 700
		self.layer = collision_layer
		self.set_hitbox_offset(6)
		self.animation_speed = 6

		#object specific
		#TODO: add formulas for attack damage
		self.bullet_clock = Clock()
		self.bullet_timer = 0
		self.bullet_delay = 150
		self.speed				= 3
		self.hp					= 99999999999
		self.mana				= 100
		self.contact_damage 	= 0
		self.damage				= 30

		#collision
		self.team = True

		#collision overwrite
		self.is_collideable[ObjectType.NULL]			=	True
		self.is_collideable[ObjectType.PLAYER]			=	True
		self.is_collideable[ObjectType.ALLY]			=	True
		self.is_collideable[ObjectType.ENEMY]			=	True
		self.is_collideable[ObjectType.SPAWNER]			=	False
		self.is_collideable[ObjectType.BULLET]			=	True
		self.is_collideable[ObjectType.CONTAINER]		=	False
		self.is_collideable[ObjectType.DECORATION]		=	False
		self.is_collideable[ObjectType.LABEL]			=	False
		self.is_collideable[ObjectType.WALL]			=	True
		self.is_collideable[ObjectType.TRAPDOOR]		=	True
		self.is_collideable[ObjectType.DIALOG]			=	False
		
		self.process_collision[ObjectType.NULL]			=	[self.bounce]
		self.process_collision[ObjectType.PLAYER]		=	[self.bounce]
		self.process_collision[ObjectType.ALLY]			=	[self.bounce]
		self.process_collision[ObjectType.ENEMY]		=	[self.bounce, self.take_damage]
		self.process_collision[ObjectType.BULLET]		=	[self.take_damage]
		self.process_collision[ObjectType.WALL]			=	[self.bounce]
		self.process_collision[ObjectType.TRAPDOOR]		=	[]
		

	def check_collideable(self, object):
		if object.type.name == 'BULLET':
			if object.team == self.team:
				return False
		return self.is_collideable[object.type]


	def every_tick(self):
		self.bullet_clock.tick()
		self.bullet_timer += self.bullet_clock.get_time()
		self.handle_input()
		return super().every_tick()
		

	def handle_input(self):
		pressed = pygame.key.get_pressed()
		mouse_pressed = pygame.mouse.get_pressed()
		speed_vector = Vector2(0.0,0.0)
		
		any = False
		if pressed[pygame.K_w]:
			speed_vector.y -= self.speed
			self.change_animation_track(1)
			any = True
			
		if pressed[pygame.K_s]:
			speed_vector.y += self.speed
			self.change_animation_track(0)
			any = True
			
		if pressed[pygame.K_a]:
			speed_vector.x -= self.speed
			self.change_animation_track(2)
			any = True
			
		if pressed[pygame.K_d]:
			speed_vector.x += self.speed
			self.change_animation_track(3)
			any = True

		if pressed[pygame.K_o]:
			self.change_animation_track(4)
			any=True
		
		if pressed[pygame.K_p]:
			self.change_animation_track(5)
			any=True

			
		
		self.movement_speed = speed_vector
		if any == False:
			self.animation_stop()
		else:
			self.animation_play()

		if mouse_pressed[0] and self.bullet_timer > self.bullet_delay:
			self.shoot()
			self.bullet_timer = 0

		if mouse_pressed[2] and self.bullet_timer > self.bullet_delay:
			x = GameObject()
			x.move(Vector2(pygame.mouse.get_pos() - (x.size/2)))
			self.bullet_timer = 0

		if mouse_pressed[1] and self.bullet_timer > self.bullet_delay:
			x = Wall()
			x.move(Vector2(pygame.mouse.get_pos() - (x.size/2)))
			self.bullet_timer = 0


	def shoot(self):
		#create bullet in the middle of player
		bullet = Bullet(self)
		bullet.move(self.position)

		#calculate where to shoot
		shooting_direction = Vector2(pygame.mouse.get_pos()) - (self.position+(self.size/2))
		shooting_direction = shooting_direction.normalize()
		try:
			bullet.movement_speed = shooting_direction*bullet.speed
			q = Vector2()
			q.from_polar(( self.hitbox_size.length()/2 + bullet.hitbox_size.length()/2,  shooting_direction.as_polar()[1]))
			bullet.move(q)
		except ValueError:
			bullet.kill()
		
