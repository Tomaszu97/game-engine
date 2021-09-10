from .resource_handler  import  *
import os

#TODO do better
basedir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(basedir) + '/'

window_size      = (800, 685)
window_position  = (5, 35)
tick = 75

display_hitboxes = False
display_borders  = False
display_names    = False
display_velocity = False

collision_layer  = 4
all_objects      = []
slowdown_factor  = 0.99
camera_position  = Vector2(0.0, 0.0)


BASEDIR = os.path.abspath(os.path.dirname(__file__))

#TODO - this is temporary
resources        = ImageController()
for filename in os.listdir(basedir + 'data/images/'):
    print(filename)
    if filename.endswith('.png'):
        newname = str(filename).split('.')[0]
        print(newname)
        setattr(resources, newname, basedir + f'data/images/{filename}')
        #resources.newname  =   basedir + f'data/images/{filename}'

#TODO - temp
print(resources)
