from .resource_handler  import  *
import os

# untouchables
basedir          = os.path.abspath(os.path.dirname(__file__)) #TODO improve basedir handling
basedir          = os.path.dirname(basedir) + '/'
cameras          = []
all_objects      = []
event_receiver_objects = []
app_running      = False
resources        = ImageController() #TODO better resource management
for filename in os.listdir(basedir + 'data/images/'):
    print(filename)
    if filename.endswith('.png'):
        newname = str(filename).split('.')[0]
        print(newname)
        setattr(resources, newname, basedir + f'data/images/{filename}')
        #resources.newname  =   basedir + f'data/images/{filename}'

# editables
window_size      = (1536,864)
#window_size      = (256,144)
#window_size      = (640,480)
window_position  = (100,100)
tick = 75
background_color = (0, 0, 0, 255)
display_hitboxes = False
display_borders  = False
display_names    = False
display_velocity = False
collision_layer  = 4
slowdown_factor  = 0.99
