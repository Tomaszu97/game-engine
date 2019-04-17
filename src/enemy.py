from game_object    import *
from shared         import *
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
        self.speed = 1
        self.sight_radius = 400

        #state related        
        self.state_clock = Clock()          # clock to measure time in states
        self.state_timer = 0                # time in actual state
        self.idle_to_patrol_time = 4000     # when to start patroling
        self.waypoint = None                # waypoint used in patroling
        self.state = self.idle              # current state of enemy
        self.attack_range = 300
        self.attack_state = None
        self.attack_list = []


    def every_tick(self):
        self.state_clock.tick()
        self.state_timer += self.state_clock.get_time()
        self.state()
        return super().every_tick()

    def choose_target(self):
        if self.target_list:
            return(random.choice(self.target_list))
        return None

    ##################### STATES ##########################
    #TODO: Add attack state

    # just standing still, after a while -> patrolling
    def idle(self):
        self.movement_speed = Vector2(0.0, 0.0)
        distance = Vector2(self.target.position - self.position).length()
        if distance < self.sight_radius:
            self.state_timer = 0
            self.state = self.follow        
        if self.state_timer > self.idle_to_patrol_time:
            self.state_timer = 0
            self.state = self.choose_waypoint
            
    # following a target if in sight range
    def follow(self):
        direction = Vector2(self.target.position - self.position)
        distance = direction.length()
        direction = direction.normalize()
        self.movement_speed = direction * self.speed
        if distance < self.attack_range:
            self.state_timer = 0
            self.attack_state = self.choose_skill
            self.state = self.attack
        elif distance > self.sight_radius:
            self.state_timer = 0
            self.state = self.idle
    
    # walking to a random waypoint
    def patrol(self):
        distance = Vector2(self.target.position - self.position).length()
        waypoint_dist = Vector2(self.waypoint - self.position)
        if distance < self.sight_radius:
            self.state_timer = 0
            self.state = self.follow
        elif waypoint_dist.length() < 50:            
            self.state_timer = 0
            self.state = self.idle 
        elif self.state_timer > 5000:  
            self.state_timer = 0
            self.state = self.idle     
        waypoint_dist = waypoint_dist.normalize()
        self.movement_speed = waypoint_dist * self.speed  

    # choosing a waypoint
    def choose_waypoint(self):
        self.waypoint = (Vector2((random.randint(0,window_size[1]), random.randint(0, window_size[0]))))  
        self.state_timer = 0
        self.state = self.patrol

    def attack(self):
        self.attack_state()

    def choose_skill(self):
        self.attack_state = random.choice(self.attack_list)
            
    ##################### SKILLS ##########################
    # TODO: Add choose_skill, exhausted, cooldown

    def charging(self, charge_time):
        pass

    def speed_boost(self):
        distance = Vector2(self.target.position - self.position)
        distance = distance.normalize()
        self.movement_speed = distance * self.speed * 3
        if self.state_timer > 2000:
            self.state_timer = 0
            self.attack_state = self.exhausted

    def exhausted(self):
        exhaust_lenght = 3000
        self.movement_speed *= 0.999
        if self.state_timer > exhaust_lenght:
            self.state_timer = 0
            self.state = self.idle 

class Enemy_Following(Enemy):
    def __init__(self, parent=None, position=Vector2(0.0, 0.0), target_list=None):
        super().__init__(parent, position, target_list)
        self.enemy_type = EnemyType.FOLLOWING
        self.set_animation_spritesheet('../data/konon.png')
        self.mass = 1000
        self.attack_list = [self.speed_boost]

    def every_tick(self):
        return super().every_tick()

class Enemy_Orbiting(Enemy):
    def __init__(self, parent=None, position=Vector2(0.0, 0.0), target_list=None):
        super().__init__(parent, position, target_list)

        self.enemy_type = EnemyType.ORBITING
        self.set_animation_spritesheet('../data/konon.png')
        self.mass = 1000

    def follow(self):
        distance = Vector2(self.target.position - self.position)
        if distance.length() > self.sight_radius:
            self.state_timer = 0
            self.state = self.idle
        distance = distance.normalize()
        distance = distance.rotate(90)   
        self.movement_speed = distance * self.speed

    def every_tick(self):
        return super().every_tick()

class Enemy_Wandering(Enemy):
    def __init__(self, parent=None, position=Vector2(0.0, 0.0), target_list=None):
        super().__init__(parent, position, target_list)

        self.enemy_type = EnemyType.WANDERING
        
        self.set_animation_spritesheet('../data/konon.png')
        self.mass = 1000
        self.idle_to_patrol_time = 500

    def idle(self):
        self.movement_speed = Vector2(0.0, 0.0)      
        distance = Vector2(self.target.position - self.position)  
        if self.state_timer > self.idle_to_patrol_time:
            self.state_timer = 0
            self.state = self.choose_waypoint
        
    def patrol(self):
        distance = Vector2(self.target.position - self.position)
        waypoint_dist = Vector2(self.waypoint - self.position)

        if waypoint_dist.length() < 50:            
            self.state_timer = 0
            self.state = self.idle 
        elif self.state_timer > 5000:  
            self.state_timer = 0
            self.state = self.idle     
            
        waypoint_dist = waypoint_dist.normalize()
        self.movement_speed = waypoint_dist * self.speed  

    def every_tick(self):
        return super().every_tick()