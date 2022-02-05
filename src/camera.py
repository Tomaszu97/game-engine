from .game_object   import *
from .shared        import *

class Camera():
    def __init__(self):
        self.window_position = [0,0]
        self.window_size = [200,100]
        self.world_position = Vector2(0,0)
        self._world_size = Vector2(200,100)
        self.surface = Surface((self._world_size.x, self._world_size.y))
        self.obj_to_follow = None
        global cameras
        cameras.append(self)

    def move_window(self, x, y):
        self.window_position[0] += x
        self.window_position[1] += y

    def move_world(self, x, y):
        self.world_position += Vector2(x,y)

    @property
    def world_size(self):
        return self._world_size

    @world_size.setter
    def world_size(self,val):
        self._world_size = val
        self.surface = Surface((self._world_size.x, self._world_size.y))

    def render(self, objects):
        if self.obj_to_follow is not None:
            self.world_position = self.obj_to_follow.position + (self.obj_to_follow.size/2) - (self.world_size/2)
        self.surface.fill(background_color)
        if all_objects:
            for layer in range(min(o.layer for o in all_objects), max(o.layer for o in all_objects)+1):
                for o in all_objects:
                    if o.layer == layer:
                        self.surface.blit(o.surface, (o.position.x - self.world_position.x, o.position.y - self.world_position.y))

    def trans_wind_to_world_pos(self, in_x, in_y):
        scale_x = self.world_size.x / self.window_size[0]
        scale_y = self.world_size.y / self.window_size[1]
        return Vector2((in_x - self.window_position[0]) * scale_x + self.world_position.x, (in_y - self.window_position[1]) * scale_y + self.world_position.y)


