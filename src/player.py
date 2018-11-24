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
		super().every_tick()
		self.handle_input()


	def handle_input(self):
			
		pressed = pygame.key.get_pressed()
		
		if pressed[pygame.K_ESCAPE]:
				self.on_cleanup()

		any = False
		if pressed[pygame.K_UP]:
			self.move(0, -self.speed)
			self.anim_change_track(1)
			any = True
			
		if pressed[pygame.K_DOWN]:
			self.move(0, self.speed)
			self.anim_change_track(0)
			any = True
			
		if pressed[pygame.K_LEFT]:
			self.move(-self.speed, 0)
			self.anim_change_track(2)
			any = True
			
		if pressed[pygame.K_RIGHT]:
			self.move(self.speed, 0)
			self.anim_change_track(3)
			any = True
			
		if any == False:
			self.anim_stop()
		else:
			self.anim_play()