from .resource_handler  import  *
import os

class _SingletonWrapper:
    """
    A singleton wrapper class. Its instances would be created
    for each decorated class.
    """

    def __init__(self, cls):
        self.__wrapped__ = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        """Returns a single instance of decorated class"""
        if self._instance is None:
            self._instance = self.__wrapped__(*args, **kwargs)
        return self._instance

def singleton(cls):
    """
    A singleton decorator. Returns a wrapper object. A call on that object
    returns a single instance object of decorated class. Use the __wrapped__
    attribute to access the decorated class directly in unit tests.
    """
    return _SingletonWrapper(cls)

@singleton
class GlobalObjects:
    def __init__(self):
        self.cameras          = []
        self.all_objects      = []
        self.event_receiver_objects = []
        self.mouseclick_receiver_objects = []

    def remove(self, obj):
        self.cameras = [x for x in self.cameras if x is not obj]
        self.all_objects = [x for x in self.all_objects if x is not obj]
        self.event_receiver_objects = [x for x in self.event_receiver_objects if x is not obj]
        self.mouseclick_receiver_objects = [x for x in self.mouseclick_receiver_objects if x is not obj]

    def clear_all(self):
        for o in self.cameras:
            del o
        for o in self.all_objects:
            del o
        for o in self.event_receiver_objects:
            del o
        for o in self.mouseclick_receiver_objects:
            del o
        self.cameras          = []
        self.all_objects      = []
        self.event_receiver_objects = []
        self.mouseclick_receiver_objects = []

# untouchables
basedir          = os.path.abspath(os.path.dirname(__file__)) #TODO improve basedir handling
basedir          = os.path.dirname(basedir) + '/'
app_instance     = None
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
debug            = False
