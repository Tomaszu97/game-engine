from src.main import *

def info_message_tr_h():
    print("here, display a button and a message")

def first_enemy_tr_h():
    EnemyFollowing(target_list = [pl], position = Vector2(135, -150))

def runner_enemy_tr_h():
    EnemyFollowing(target_list = [pl], position = Vector2(15, -12))

def finish_tr_h():
    print("go to new level")

TiledManager().load_map(basedir + 'data/maps/level1.tmx')

pygame.mixer.music.load('data/music/focus.ogg')
pygame.mixer.music.play(-1)

pl = Player()
pl.hitbox_offset = Vector2(pl.size.x/6, pl.size.y/4)
pl.hitbox_size = Vector2(pl.size.x*4/6, pl.size.y*3/4)
pl.move(30, -370)

start_tr = Trapdoor()
start_tr.move(70, -247)
start_tr.reset()
start_tr.set_handler(info_message_tr_h)

first_enemy_tr = Trapdoor()
first_enemy_tr.move(15, -175)
first_enemy_tr.reset()
first_enemy_tr.set_handler(first_enemy_tr_h)

runner_enemy_tr = Trapdoor()
runner_enemy_tr.move(15, 70)
runner_enemy_tr.reset()
runner_enemy_tr.set_handler(runner_enemy_tr_h)

finish_tr = Trapdoor()
finish_tr.move(1025, 200)
finish_tr.reset()
finish_tr.set_handler(finish_tr_h)

#code.interact(local=locals())
