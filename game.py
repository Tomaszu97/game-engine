from src.main import *

TiledManager().load_map(basedir + 'data/maps/level1.tmx')

pl = Player()
tr = Trapdoor()
tr2 = Trapdoor()
tr.move(200,200)
tr2.move(200,350)
tr.reset()
tr2.reset()

def f():
    print('spawning enemies...')
    EnemyFollowing(target_list = [pl], position = Vector2(200.0,400.0))
    EnemyFollowing(target_list = [pl], position = Vector2(400.0,200.0))
    EnemyFollowing(target_list = [pl], position = Vector2(400.0,400.0))
tr.set_handler(f)

def g():
    print('resetting tr...')
    tr.reset()
    tr2.reset()
tr2.set_handler(g)

#code.interact(local=locals())
