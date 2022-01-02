from .game_object   import *
from .shared        import *
import weakref

class ResourceController(object):
    def __init__(self, loader):
        self.__dict__.update(dict(
            names = {},
            cache = weakref.WeakValueDictionary(),
            loader = loader
        ))

    def __setattr__(self, name, value):
        self.names[name] = value

    def __getattr__(self, name):
        try:
            img = self.cache[name]
        except KeyError:
            img = self.loader(self.names[name])
            self.cache[name] = img
        return img

class ImageController(ResourceController):
    def __init__(self):
        ResourceController.__init__(self, pygame.image.load)
