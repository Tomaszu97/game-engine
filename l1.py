from src.main import *

def first_enemy_tr_h(trap, prey):
    EnemyFollowing(target_list = [pl], position = Vector2(135, -150))

def runner_enemy_tr_h(trap, prey):
    EnemyFollowing(target_list = [pl], position = Vector2(15, -12))

def runner_enemy_2_tr_h(trap, prey):
    EnemyFollowing(target_list = [pl], position = Vector2(335, 40))

def runner_enemy_3_tr_h(trap, prey):
    EnemyFollowing(target_list = [pl], position = Vector2(430, 340))

def runner_enemy_4_tr_h(trap, prey):
    EnemyFollowing(target_list = [pl], position = Vector2(865, 245))
    EnemyFollowing(target_list = [pl], position = Vector2(995, 245))
    EnemyFollowing(target_list = [pl], position = Vector2(895, 190))

TiledManager().load_map(basedir + 'data/maps/level1.tmx')

pygame.mixer.music.load('data/music/focus.ogg')
pygame.mixer.music.play(-1)

pl = Player()
pl.position = Vector2(30, -370)
pl.hitbox_offset = Vector2(pl.size.x/6, pl.size.y/4)
pl.hitbox_size = Vector2(pl.size.x*4/6, pl.size.y*3/4)

start_tr = Trapdoor()
start_tr.position = Vector2(30, -370)
def info_message_tr_start(trap, prey):
    la = Label()
    la.size = Vector2(70,40)
    la.position = Vector2(-80,-410)
    la.text = ' hello there!\n welcome to\n    DING'

    bt = Button()
    bt.position = Vector2(-57,-365)
    bt.size = Vector2(23,15)
    bt.text = ' ok'
            
    pl.speed = 0
    pl.bullet_delay = float('inf')
    
    def bthandler():
        if 'WSAD' not in la.text:
            la.size = Vector2(la.size.x, la.size.y+20)
            la.text = 'use WSAD to move\nuse mouse to shoot'
            bt.move(0,20)
        else:
            la.kill()
            bt.kill()
            pl.speed = 1.5
            pl.bullet_delay = 400
    bt.handler = bthandler
start_tr.set_handler(info_message_tr_start)


tr1= Trapdoor()
tr1.position = Vector2(75, -280)
def info_message_tr_1(trap, prey):
    pl.speed = 0
    pl.bullet_delay = float('inf')
    la = Label()
    la.position = Vector2(-40,-310)
    la.size = Vector2(70,90)
    la.text = 'at the time of your journey you will encounter enemies'
    bt = Button()
    bt.position = Vector2(-17, -215)
    bt.size = Vector2(23,15)
    bt.text = ' ok'
    def bthandler():
        if 'KILL' not in la.text:
            la.size = Vector2(la.size.x, la.size.y-60)
            la.bg_color, la.text_color = la.text_color, la.bg_color 
            la.text = '    KILL\n    THEM'
            bt.move(0,-60)
        else:
            la.kill()
            bt.kill()
            pl.speed = 1.5
            pl.bullet_delay = 400
    bt.handler = bthandler
tr1.set_handler(info_message_tr_1)

first_enemy_tr = Trapdoor()
first_enemy_tr.position = Vector2(15, -175)
first_enemy_tr.set_handler(first_enemy_tr_h)

runner_enemy_tr = Trapdoor()
runner_enemy_tr.position = Vector2(15, 70)
runner_enemy_tr.set_handler(runner_enemy_tr_h)

runner_enemy_2_tr = Trapdoor()
runner_enemy_2_tr.position = Vector2(335, 80)
runner_enemy_2_tr.set_handler(runner_enemy_2_tr_h)

runner_enemy_3_tr = Trapdoor()
runner_enemy_3_tr.position = Vector2(550, 340)
runner_enemy_3_tr.set_handler(runner_enemy_3_tr_h)

runner_enemy_4_tr = Trapdoor()
runner_enemy_4_tr.position = Vector2(840, 340)
runner_enemy_4_tr.set_handler(runner_enemy_4_tr_h)

def heal_tr_h(trap, prey):
    prey.hp += 40
    if prey.hp > prey.max_hp:
        prey.hp = prey.max_hp
    trap.kill()
heal_tr = Trapdoor()
heal_tr.position = Vector2(425, 233)
heal_tr.set_animation_spritesheet(resources.heal)
heal_tr.set_handler(heal_tr_h)
heal_2_tr = Trapdoor()
heal_2_tr.position = Vector2(745, 343)
heal_2_tr.set_animation_spritesheet(resources.heal)
heal_2_tr.set_handler(heal_tr_h)

finish_tr = Trapdoor()
finish_tr.position = Vector2(1045, 170)
finish_tr.size = Vector2(50,100)
finish_tr.set_scaled_hitbox_offset(0)
def finish_tr_h(trap, prey):
    global all_objects
    all_objects.clear()
    pygame.mixer.music.stop()
finish_tr.set_handler(finish_tr_h)

big_camera = Camera()
big_camera.world_size = Vector2(256,144)
big_camera.move_world(30, -370)
big_camera.window_size = Vector2(big_camera.world_size*6)
big_camera.obj_to_follow = pl
