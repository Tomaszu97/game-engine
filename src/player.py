from game_object import *
from bullet import *
from shared import *
import math

class Player(GameObject):
	def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
		super().__init__(parent, position)
		self.type =	ObjectType.PLAYER
		self.name = 'player'

		self.clock1 = Clock()
		self.bullet_timer = .3
		self.speed	=	7
		self.mass = 36
		self.hp		=	100
		self.mana	=	100
		
		#initial
		self.animation_grid = [4,8]
		self.set_animation_spritesheet('../data/scaled_xbr.png')
		

	def every_tick(self):
		self.handle_input()
		super().every_tick()
		

	def handle_input(self):
		dt = self.clock1.tick(75) / 1000
		pressed = pygame.key.get_pressed()
		mouse_pressed = pygame.mouse.get_pressed()
		self.bullet_timer -= dt
		
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
		
		self.movement_speed = speed_vector

		if any == False:
			self.animation_stop()
		else:
			self.animation_play()

		if self.bullet_timer <= 0:
			if mouse_pressed[0]:
				self.shoot()


	def shoot(self):
		#create bullet in the middle of player
		bullet = Bullet(self)
		bullet.move( (self.position+(self.size/2) - bullet.size/2))
		
		#can use reversing bullets :O
		bullet.speed = 10
		#bullet.acceleration = -0.2

		#calculate where to shoot
		shooting_direction = Vector2(pygame.mouse.get_pos()) - (self.position+(self.size/2))
		shooting_direction = shooting_direction.normalize()

		try:
			bullet.movement_speed = shooting_direction*bullet.speed
			bullet.movement_acceleration = shooting_direction*bullet.acceleration
			q = Vector2()
			q.from_polar(( self.hitbox_size.length()/2 + bullet.hitbox_size.length()/2,  shooting_direction.as_polar()[1]))
			bullet.move(q)
		except ValueError:
			y.kill()

		self.bullet_timer = .1
		