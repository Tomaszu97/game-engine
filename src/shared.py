from resource_handler  import  *
import os

window_size      = (800, 685)
window_position  = (5, 35)
tick = 75
background_color = (255,127,80,255)

display_hitboxes = False
display_borders  = False
display_names    = False
display_velocity = False

collision_layer  = 4

all_objects      = []
event_receiver_objects = []
slowdown_factor  = 0.99

BASEDIR = os.path.abspath(os.path.dirname(__file__))

#TODO - this is temporary
resources = ImageController()
for filename in os.listdir(f'{BASEDIR}/../data/images/'):
    #print(filename)
    if filename.endswith('.png'):
        newname = str(filename).split('.')[0]
        #print(newname)
        setattr(resources, newname, f'{BASEDIR}/../data/images/{filename}')
        #resources.newname  =   f'../data/images/{filename}'

#TODO - temp
print(resources)
