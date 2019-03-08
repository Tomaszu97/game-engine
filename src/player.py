from game_object import *
from bullet import *

class Player(GameObject):
	def __init__(self, parent):
		super().__init__(parent)
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


	def every_tick(self):
		self.handle_input()
		super().every_tick()
		


	def handle_input(self):
			
		pressed = pygame.key.get_pressed()
		mouse_pressed = pygame.mouse.get_pressed()
		
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

		if mouse_pressed[0]:
			self.shoot()


	def shoot(self):
		Bullet(self)