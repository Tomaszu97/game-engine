from pygame import Rect
import shared

class Collision_Manager():
	def __init__(self):
		self.collision_resolver = Collision_Resolver()

	def check_collision(self, object, other_object):
		if object.check_collideable(other_object):
			if not object.to_kill:
				if Rect(object.hitbox_position, object.hitbox_size).colliderect(Rect(other_object.hitbox_position, other_object.hitbox_size)):
					self.collision_resolver.resolve_collision(object, other_object)

	def check_all(self, to_collide):
		for object in to_collide:
			for other_object in to_collide:
				if object is not other_object:
					self.check_collision(object, other_object)


class Collision_Resolver():
	# check what happens after a collision
	def resolve_collision(self, object, other_object):
		functions = object.get_on_collide(other_object)
		if functions:
			for name in functions:
				# because bounce is in Collision_Resolver class
				if name == 'bounce':
					self.bounce(object, other_object)
				else:
					# invokes object.name(other_object)
					getattr(object, name)(other_object)


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
						
		