import pyglet
import random


class PhysicalObject(pyglet.shapes.Line):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0
    
    def update(self):
        self.y -= 5
        self.check_bounds()

    def check_bounds(self):
        min_y = 0
        max_y = random.randint(100,1200)
        max_velocity = 100 
        if self.y <= min_y:
            self.y = max_y


