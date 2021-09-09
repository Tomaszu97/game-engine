from pygame        import Rect
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
            for function in functions:
                function(object, other_object)
            return True
        return False

