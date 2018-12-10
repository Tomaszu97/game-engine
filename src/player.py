from game_object import *

class Player(GameObject):
	def __init__(self, id):
		super().__init__(id)
		self.type =	ObjectType.PLAYER
		
		#object specific
		self.speed	=	7
		self.hp		=	100
		self.mana	=	100
		#defense and attack depends on equipped stuff


	def every_tick(self):
		self.handle_input()
		super().every_tick()
		


	def handle_input(self):
			
		pressed = pygame.key.get_pressed()
		
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