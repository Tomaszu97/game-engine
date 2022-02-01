from pygame        import Rect
from .shared       import *
from .game_object  import *
import math

class CollisionManager():
    #TODO first load the whole level ,then handle this stuff, otherwise race condition sometimes happens
    def __init__(self):
        # collision handlers

        # elastic collision
        def BNC(object, other_object, elastic=True):
            sign = lambda x: 1 if x>=0 else -1

            # return if object width or height is 0
            if other_object.hitbox_size.x == 0 or other_object.hitbox_size.y == 0:
                return

            # move them away and collide
            if Rect(object.hitbox_position, object.hitbox_size).colliderect(Rect(other_object.hitbox_position, other_object.hitbox_size)):
                relative_position = object.position + (object.size/2) - other_object.position - (other_object.size/2)
                total_speed = object.movement_speed + other_object.movement_speed

                if object.mass == 0 or other_object.mass == 0:
                    mass_ratio = 1
                    other_mass_ratio = 1
                else:
                    mass_ratio = object.mass / (object.mass+other_object.mass)
                    other_mass_ratio = other_object.mass / (object.mass+other_object.mass)  

                # relpos from other to me
                if relative_position.x < 0:
                    # self approach from the left
                    x_intersection = -round(object.hitbox_position.x+object.hitbox_size.x-other_object.hitbox_position.x)
                else:
                    # self approach from the right
                    x_intersection = round(other_object.hitbox_position.x+other_object.hitbox_size.x-object.hitbox_position.x)
                if relative_position.y < 0:
                    # self approach from above
                    y_intersection = -round(object.hitbox_position.y+object.hitbox_size.y-other_object.hitbox_position.y)
                else:
                    # self approach from below
                    y_intersection = round(other_object.hitbox_position.y+other_object.hitbox_size.y-object.hitbox_position.y)

                #TODO optimize it
                #TODO make ceil round "up" for negatives as well
                if abs(x_intersection) > abs(y_intersection):
                    if object.mass != 0:
                        object.move(0, math.ceil(y_intersection*other_mass_ratio))
                        if elastic:
                            object.movement_speed.y = sign(y_intersection)*abs(other_mass_ratio*total_speed.y)
                        else:
                            object.movement_speed.y = 0
                    if other_object.mass != 0:
                        other_object.move(0, math.ceil(-y_intersection*mass_ratio))
                        if elastic:
                            other_object.movement_speed.y = -sign(y_intersection)*abs(mass_ratio*total_speed.y)
                        else:
                            other_object.movement_speed.y = 0
                else:
                    if object.mass != 0:
                        object.move(math.ceil(x_intersection*other_mass_ratio), 0)
                        if elastic:
                            object.movement_speed.x = sign(x_intersection)*abs(other_mass_ratio*total_speed.x)
                        else:
                            object.movement_speed.x = 0
                    if other_object.mass != 0:
                        other_object.move(math.ceil(-x_intersection*mass_ratio), 0)
                        if elastic:
                            other_object.movement_speed.x = -sign(x_intersection)*abs(mass_ratio*total_speed.x)
                        else:
                            other_object.movement_speed.x = 0

        # inelastic collision
        def HIT(object, other_object):
            return BNC(object, other_object, elastic=False)

        # take damage - first object takes damage
        def TDM(object, other_object):
            try:
                object.hp -= other_object.damage
                if object.hp < 0:
                    object.kill()
            except AttributeError:
                return

        # make damage - second object takes damage
        def MDM(object, other_object):
            return TDM(other_object, object)

        # kill yourself
        def KYS(object, other_object):
            object.kill()

        # kill him
        def KHM(object, other_object):
            return KYS(other_object, object)

        # teamwork - stop processing collision if both objects are in the same team
        def TMW(object, other_object):
            # stop processing collision if both are in the same team
            if object.team == other_object.team:
                return False

        # call trapdoor handler if trapdoor is not triggered
        def TRP(object, other_object):
            # optimize it - maybe take advantage of collision order (higher first)
            if object.type == TRAPDOOR:
                trapdoor = object
            else:
                trapdoor = other_object
            if not trapdoor.triggered:
                trapdoor.triggered = True
                trapdoor.handler()

        # bullet kys - kill a bullet
        def BKS(object, other_object):
            # optimize it
            if object.type == BULLET:
                bullet = object
            else:
                bullet = other_object
            bullet.kill()  

        # matrix defining collision behavior
        self.collision_matrix = [
        # NULL      PLAYER         ALLY           ENEMY          SPAWNER  BULLET CONTAINER DECORATION   LABEL WALL  TRAPDOOR DIALOG TEXTINPUT
        [ [HIT],                                                                                                                             ],# NULL
        [ [HIT],    None,                                                                                                                    ],# PLAYER
        [ None,     None,          None,                                                                                                     ],# ALLY
        [ None,     [HIT,MDM],     [HIT,MDM],     None,                                                                                      ],# ENEMY
        [ None,     None,          None,          None,          None,                                                                       ],# SPAWNER
        [ None,     [TMW,MDM,BKS], [TMW,MDM,BKS], [TMW,MDM,BKS], None,    None,                                                              ],# BULLET
        [ None,     [HIT],         [HIT],         None,          None,    None,  None,                                                       ],# CONTAINER
        [ None,     None,          None,          None,          None,    None,  None,     None,                                             ],# DECORATION
        [ None,     None,          None,          None,          None,    None,  None,     None,        None,                                ],# LABEL
        [ [HIT],    [HIT],         [HIT],         [HIT],         None,    [BNC], [HIT],    None,        None, None,                          ],# WALL
        [ None,     [TRP],         None,          None,          None,    None,  None,     None,        None, None, None,                    ],# TRAPDOOR
        [ None,     None,          None,          None,          None,    None,  None,     None,        None, None, None,    None,           ],# DIALOG
        [ None,     None,          None,          None,          None,    None,  None,     None,        None, None, None,    None,  None,    ],# TEXTINPUT
        ]

    def get_on_collide(self, object, other_object):
        #TODO - handle invincibility
        # if self.is_invincible:
        #   self.process_collision[str(object.type.name)][:-1]
        srt = sorted([object.type, other_object.type], reverse=True)
        return self.collision_matrix[srt[0]][srt[1]]

    def handle_collision(self, object, other_object):
        functions = self.get_on_collide(object, other_object)
        if functions:
            if Rect(object.hitbox_position, object.hitbox_size).colliderect(Rect(other_object.hitbox_position, other_object.hitbox_size)):
                for function in functions:
                    srt = sorted([object, other_object], key=lambda x: x.type, reverse=True)  # pass object with higher type number as first parameter
                    if function(srt[0], srt[1]) is False: break                               # break when one of the handlers returns False
                return True
        return False

    #TODO optimize it
    def handle_all_collisions(self, to_collide):
        for object in to_collide:
            for other_object in to_collide:
                if object is not other_object:
                    self.handle_collision(object, other_object)

