from resource_handler  import  *
import os

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

#TODO - this is temporary
resources        = ImageController()
for filename in os.listdir('../data/images/'):
    print(filename)
    if filename.endswith('.png'):
        newname = str(filename).split('.')[0]
        print(newname)
        setattr(resources, newname, f'../data/images/{filename}')
        #resources.newname  =   f'../data/images/{filename}'

#TODO - temp
print(resources)
