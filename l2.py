from cgitb import small
from src.main import *

TiledManager().load_map(basedir + 'data/maps/level2.tmx')

pygame.mixer.music.load('data/music/terribleterror.ogg')
pygame.mixer.music.play(-1)

pl = Player()
pl.hitbox_offset = Vector2(pl.size.x/6, pl.size.y/4)
pl.hitbox_size = Vector2(pl.size.x*4/6, pl.size.y*3/4)
pl.move(-135, -405)

start_tr = Trapdoor()
start_tr.move(70, -247)
start_tr.reset()
shooting_pos_tr = Trapdoor()
shooting_pos_tr.move(15, -175)
shooting_pos_tr.reset()

big_camera = Camera()
big_camera.world_size = Vector2(256,144)
big_camera.window_size = Vector2(big_camera.world_size*6)
big_camera.obj_to_follow = pl

small_camera = Camera()
small_camera.world_size = Vector2(96,54)
small_camera.move_world(30, -370)
small_camera.window_size = Vector2(small_camera.world_size*6)
small_camera.window_position = [window_size[0]*2/3 - 12, window_size[1]*2/3 - 12]

w1 = GameObject()
w1.mass = 0
w1.move(-235, -504)
w1.set_size( Vector2(8, 3) )
w1.set_animation_spritesheet_blank(Color(0,0,0,0))

w2 = GameObject()
w2.mass = 0
w2.move(-219, -504)
w2.set_size( Vector2(8, 3) )
w2.set_animation_spritesheet_blank(Color(0,0,0,0))


w3 = GameObject()
w3.mass = 0
w3.move(-244, -518)
w3.set_size( Vector2(9, 17) )
w3.set_animation_spritesheet_blank(Color(0,0,0,0))


w4 = GameObject()
w4.mass = 0
w4.move(-211, -518)
w4.set_size( Vector2(9, 17) )
w4.set_animation_spritesheet_blank(Color(0,0,0,0))


def info_message_tr_h():
    print("here, display a button and a message")
start_tr.set_handler(info_message_tr_h)

def shooting_pos_tr_h():
    EnemyFollowing(target_list = [pl], position = Vector2(135, -150))
shooting_pos_tr.set_handler(shooting_pos_tr_h)

#TODO finish on enemy killed
en = EnemyFollowing(target_list = [pl], position = Vector2(-495, -875))
#pl.position = Vector2(-520, 875)


while True:
    lastbullet = None
    for i in range(len(pl.children)-1, -1, -1):
        lastbullet = pl.children[i]
        if lastbullet.type == BULLET:
            small_camera.window_position = [window_size[0]*2/3 - 12, window_size[1]*2/3 - 12]
            small_camera.obj_to_follow = lastbullet
            lastbullet.slowdown_factor = 1
            lastbullet.ttl = 5000
            break
    else:
        small_camera.window_position = [window_size[0]+10, window_size[1]*2/3 - 12]
    time.sleep(0.1)
