from game_object import *
from bullet import *
import math

class Player(GameObject):
	def __init__(self, parent):
		super().__init__(parent)
		self.clock1 = Clock()
		self.type =	ObjectType.PLAYER
		
		#object specific
		#defense and attack depends on equipped stuff
		self.speed	=	7
		self.mass = 36
		self.hp		=	100
		self.mana	=	100

		
		#TODO - delete this - temporary
		self.animation_grid = [4,8]
		self.anim_set_spritesheet('../data/scaled_xbr.png')
		self.display_border = True
		self.display_hitbox = True
		self.display_name = True
		self.movement_speed_vector = Vector2(1,2)

		

		self.bullet_timer = .3


	def every_tick(self):
		self.handle_input()
		super().every_tick()
		


	def handle_input(self):
			
		dt = self.clock1.tick(75) / 1000
		pressed = pygame.key.get_pressed()
		mouse_pressed = pygame.mouse.get_pressed()

		self.bullet_timer -= dt
		
		if pressed[pygame.K_ESCAPE]:
				self.on_cleanup()

		speed_vector = Vector2(0,0)
		any = False

		if pressed[pygame.K_UP]:
			speed_vector.y -= self.speed
			self.anim_change_track(1)
			any = True
			
		if pressed[pygame.K_DOWN]:
			speed_vector.y += self.speed
			self.anim_change_track(0)
			any = True
			
		if pressed[pygame.K_LEFT]:
			speed_vector.x -= self.speed
			self.anim_change_track(2)
			any = True
			
		if pressed[pygame.K_RIGHT]:
			speed_vector.x += self.speed
			self.anim_change_track(3)
			any = True
		
		self.movement_speed_vector = speed_vector

		if any == False:
			self.anim_stop()
		else:
			self.anim_play()

		if self.bullet_timer <= 0:
			if mouse_pressed[0]:
				self.shoot()


	def shoot(self):
		xa, ya = Vector2(pygame.mouse.get_pos()) - self.rect.center
		angle = math.degrees(math.atan2(xa, ya))	
		y = Bullet(self, self.rect.x, self.rect.y)
		y.surface = pygame.transform.rotate(y.original_surf, angle)
		y.movement_speed_vector = Vector2(xa//10, ya//10)
		self.bullet_timer = .3