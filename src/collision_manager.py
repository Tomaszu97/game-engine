from pygame        import Rect
from .shared       import *
from .game_object  import *
import math

class CollisionManager():
    #TODO confirmed race condition -  wait for obj readiness
    def __init__(self):
        # collision handlers

        # elastic collision
        def BNC(obj, othr_obj, elastic=True):
            sign = lambda x: 1 if x>=0 else -1

            # return if obj width or height is 0
            if othr_obj.hitbox_size.x == 0 or othr_obj.hitbox_size.y == 0:
                return

            # move them away and collide
            if Rect(obj.hitbox_position, obj.hitbox_size).colliderect(Rect(othr_obj.hitbox_position, othr_obj.hitbox_size)):
                relative_position = obj.position + (obj.size/2) - othr_obj.position - (othr_obj.size/2)
                total_speed = obj.movement_speed + othr_obj.movement_speed

                if obj.mass == 0 or othr_obj.mass == 0:
                    mass_ratio = 1
                    other_mass_ratio = 1
                else:
                    mass_ratio = obj.mass / (obj.mass+othr_obj.mass)
                    other_mass_ratio = othr_obj.mass / (obj.mass+othr_obj.mass)  

                # relpos from other to me
                if relative_position.x < 0:
                    # self approach from the left
                    x_intersection = -round(obj.hitbox_position.x+obj.hitbox_size.x-othr_obj.hitbox_position.x)
                else:
                    # self approach from the right
                    x_intersection = round(othr_obj.hitbox_position.x+othr_obj.hitbox_size.x-obj.hitbox_position.x)
                if relative_position.y < 0:
                    # self approach from above
                    y_intersection = -round(obj.hitbox_position.y+obj.hitbox_size.y-othr_obj.hitbox_position.y)
                else:
                    # self approach from below
                    y_intersection = round(othr_obj.hitbox_position.y+othr_obj.hitbox_size.y-obj.hitbox_position.y)

                #TODO optimize it
                def double_sided_floor(value):
                    if value < 0:
                        return math.ceil(value)
                    else:
                        return math.floor(value)

                if abs(x_intersection) > abs(y_intersection):
                    if obj.mass != 0:
                        obj.move(0, double_sided_floor(y_intersection*other_mass_ratio))
                        if elastic:
                            obj.movement_speed.y = sign(y_intersection)*abs(other_mass_ratio*total_speed.y)
                        else:
                            obj.movement_speed.y = 0
                    if othr_obj.mass != 0:
                        othr_obj.move(0, double_sided_floor(-y_intersection*mass_ratio))
                        if elastic:
                            othr_obj.movement_speed.y = -sign(y_intersection)*abs(mass_ratio*total_speed.y)
                        else:
                            othr_obj.movement_speed.y = 0
                else:
                    if obj.mass != 0:
                        obj.move(double_sided_floor(x_intersection*other_mass_ratio), 0)
                        if elastic:
                            obj.movement_spaaaaeed.x = sign(x_intersection)*abs(other_mass_ratio*total_speed.x)
                        else:
                            obj.movement_speed.x = 0
                    if othr_obj.mass != 0:
                        othr_obj.move(double_sided_floor(-x_intersection*mass_ratio), 0)
                        if elastic:
                            othr_obj.movement_speed.x = -sign(x_intersection)*abs(mass_ratio*total_speed.x)
                        else:
                            othr_obj.movement_speed.x = 0

        # inelastic collision
        def HIT(obj, othr_obj):
            return BNC(obj, othr_obj, elastic=False)

        # take damage - first obj takes damage
        def TDM(obj, othr_obj):
            try:
                obj.hp -= othr_obj.damage
                if obj.hp < 0:
                    obj.kill()
                if othr_obj.type == BULLET:
                    othr_obj.kill()
            except AttributeError as e:
                print(e)

        # make damage - second obj takes damage
        def MDM(obj, othr_obj):
            return TDM(othr_obj, obj)

        # kill yourself
        def KYS(obj, othr_obj):
            obj.kill()

        # kill him
        def KHM(obj, othr_obj):
            return KYS(othr_obj, obj)

        # teamwork - stop processing collision if both objs are in the same team
        def TMW(obj, othr_obj):
            # stop processing collision if both are in the same team
            if obj.team == othr_obj.team:
                return False

        # call trapdoor handler if trapdoor is not triggered
        def TRP(obj, othr_obj):
            # optimize it - maybe take advantage of collision order (higher first)
            if obj.type != TRAPDOOR:
                obj, othr_obj = othr_obj, obj
            if not obj.triggered:
                obj.triggered = True
                obj.handler(obj, othr_obj)

        # matrix defining collision behavior
        self.collision_matrix = [
        # NULL      PLAYER         ALLY           ENEMY          SPAWNER  BULLET CONTAINER DECORATION   LABEL WALL  TRAPDOOR DIALOG TEXTINPUT
        [ [HIT],                                                                                                                             ],# NULL
        [ [HIT],    None,                                                                                                                    ],# PLAYER
        [ None,     None,          None,                                                                                                     ],# ALLY
        [ None,     [HIT],         [HIT],         None,                                                                                      ],# ENEMY
        [ None,     None,          None,          None,          None,                                                                       ],# SPAWNER
        [ None,     [TMW,MDM],     [TMW,MDM],     [TMW,MDM],     None,    None,                                                              ],# BULLET
        [ None,     [HIT],         [HIT],         None,          None,    None,  None,                                                       ],# CONTAINER
        [ None,     None,          None,          None,          None,    None,  None,     None,                                             ],# DECORATION
        [ None,     None,          None,          None,          None,    None,  None,     None,        None,                                ],# LABEL
        [ [HIT],    [HIT],         [HIT],         [HIT],         None,    [BNC], [HIT],    None,        None, None,                          ],# WALL
        [ None,     [TRP],         None,          None,          None,    None,  [TRP],    None,        None, None, None,                    ],# TRAPDOOR
        [ None,     None,          None,          None,          None,    None,  None,     None,        None, None, None,    None,           ],# DIALOG
        [ None,     None,          None,          None,          None,    None,  None,     None,        None, None, None,    None,  None,    ],# TEXTINPUT
        ]

    def get_on_collide(self, obj, othr_obj):
        #TODO - handle invincibility
        # if self.is_invincible:
        #   self.process_collision[str(obj.type.name)][:-1]
        srt = sorted([obj.type, othr_obj.type], reverse=True)
        return self.collision_matrix[srt[0]][srt[1]]

    def handle_collision(self, obj, othr_obj):
        functions = self.get_on_collide(obj, othr_obj)
        if functions:
            if Rect(obj.hitbox_position, obj.hitbox_size).colliderect(Rect(othr_obj.hitbox_position, othr_obj.hitbox_size)):
                for function in functions:
                    srt = sorted([obj, othr_obj], key=lambda x: x.type, reverse=True)  # pass obj with higher type number as first parameter
                    if function(srt[0], srt[1]) is False: break                               # break when one of the handlers returns False
                return True
        return False

    #TODO optimize it
    def handle_all_collisions(self, to_collide):
        for obj in to_collide:
            for othr_obj in to_collide:
                if obj is not othr_obj:
                    self.handle_collision(obj, othr_obj)

