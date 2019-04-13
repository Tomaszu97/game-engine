from game_object import *
import random

class EnemyType(Enum):
    NULL        = 0
    WANDERING   = 1
    FOLLOWING   = 2
    STATIONERY  = 3
    ORBITING    = 4
    ESCAPING    = 5 


class Enemy(GameObject):
    def __init__(self, parent=None, position=Vector2(0.0, 0.0), target_list=None):
        super().__init__(parent, position)

        self.type = ObjectType.ENEMY

        self.target_list = target_list
        self.target = self.choose_target()

        #object specific
        self.hp = 20
        self.speed = 2

    # TODO: if there is no target enemy stops moving/starts wandering
    def every_tick(self):
        #if not target_list:
            #self.target = None
        return super().every_tick()

    def choose_target(self):
        if self.target_list:
            return(random.choice(self.target_list))
        return None


class Enemy_Following(Enemy):
    def __init__(self, parent=None, position=Vector2(0.0, 0.0), target_list=None):
        super().__init__(parent, position, target_list)

        self.enemy_type = EnemyType.FOLLOWING
        self.set_animation_spritesheet('../data/konon.png')

        self.mass = 1000

    def every_tick(self):
        if self.target:
            direction = Vector2(self.target.position - self.position)
            direction = direction.normalize()
            self.movement_speed = direction * self.speed
        return super().every_tick()


class Enemy_Orbiting(Enemy):
    def __init__(self, parent=None, position=Vector2(0.0, 0.0), target_list=None):
        super().__init__(parent, position, target_list)

        self.enemy_type = EnemyType.ORBITING
        self.set_animation_spritesheet('../data/konon.png')

        self.mass = 1000

    def every_tick(self):
        if self.target:
            direction = Vector2(self.target.position - self.position)
            direction = direction.normalize()
            direction = direction.rotate(90)               
            self.movement_speed = direction * self.speed
        return super().every_tick()


class Enemy_Wandering(Enemy):
    def __init__(self, parent=None, position=Vector2(0.0, 0.0), target_list=None):
        super().__init__(parent, position, target_list)

        self.enemy_type = EnemyType.WANDERING
        self.set_animation_spritesheet('../data/konon.png')

        self.mass = 1000

        # changing a direction after a while
        self.direction_clock = Clock()
        self.direction_timer = 0
        self.direction_delay = 1000

        self.direction = Vector2((random.randint(-100,100), random.randint(-100,100)))
        self.direction.normalize()
        self.movement_speed = self.direction * self.speed

    def every_tick(self):
        self.direction_clock.tick()
        self.direction_timer += self.direction_clock.get_time()

        if self.direction_timer > self.direction_delay:
            direction = Vector2((random.randint(-100,100), random.randint(-100,100)))
            direction = direction.normalize()  
            self.direction = direction         
            self.direction_timer = 0
            self.direction_delay = random.randint(200, 2000)
        self.movement_speed = self.direction * self.speed    
        return super().every_tick()