from .game_object   import *
from .label         import *
from .shared        import *

class Button(Label):
    def __init__(self, parent = None, position = Vector2(0.0, 0.0)):
        super().__init__(parent, position)
        # object specific
        self.handler = None
        global mouseclick_receiver_objects
        mouseclick_receiver_objects.append(self)

    def on_click(self):
        if self.handler is not None:
            self.handler()
        