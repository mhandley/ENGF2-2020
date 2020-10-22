# Simple Frogger Game.  Mark Handley, UCL, 2018

from tkinter import *
from fr_model import Model
from fr_view import View
from fr_settings import Direction
import time

class Controller():
    def __init__(self):
        self.root = Tk();
        self.windowsystem = self.root.call('tk', 'windowingsystem')
        self.views = []
        self.root.bind_all('<Key>', self.key)
        self.running = True
        self.score = -1
        self.level = -1
        self.river_objects = []
        self.cars = []
        self.model = Model(self);
        self.add_view(View(self.root, self))
        self.model.activate()

    def register_river_object(self, obj):
        self.river_objects.append(obj)
        for view in self.views:
            view.register_river_object(obj)

    def register_car(self, car):
        self.cars.append(car)
        for view in self.views:
            view.register_car(car)

    def unregister_objects(self):
        self.river_objects.clear()
        for view in self.views:
            view.unregister_objects()

    def register_frog(self, frog):
        self.frog = frog
        for view in self.views:
            view.register_frog(frog)

    def add_view(self, view):
        self.views.append(view)
        view.register_frog(self.frog)
        for obj in self.river_objects:
            view.register_river_object(obj)
        for car in self.cars:
            view.register_car(car)

    #some helper functions to hide the controller implementation from
    #the model and the controller
    def update_score(self, score):
        self.score = score

    def get_score(self):
        return self.score
        
    def update_level(self, level, end_time):
        self.level = level
        for view in self.views:
            view.reset_level(end_time)

    def get_level(self):
        return self.level

    def update_lives(self, lives):
        self.lives = lives

    def get_lives(self):
        return self.lives

    def frog_is_home(self, x, y):
        for view in self.views:
            view.frog_is_home(x, y)

    def died(self):
        for view in self.views:
            view.died()

    def game_over(self):
        for view in self.views:
            view.game_over()
        
    def key(self, event):
        if event.char == 'a' or event.keysym == 'Left':
            self.model.move_frog(Direction.LEFT)
        elif event.char == 's' or event.keysym == 'Up':
            self.model.move_frog(Direction.UP)
        elif event.char == 'd' or event.keysym == 'Down':
            self.model.move_frog(Direction.DOWN)
        elif event.char == 'f' or event.keysym == 'Right':
            self.model.move_frog(Direction.RIGHT)
        elif event.char == 'q':
            self.running = False
        elif event.char == 'r':
            for view in self.views:
                view.clear_messages()
            self.model.restart()

    def run(self):
        i = 0
        last_time = time.time()
        while self.running:
            self.model.update()
            for view in self.views:
                view.update()
            self.root.update()
            i = i + 1
            if i == 60:
                t = time.time()
                elapsed = t - last_time
                last_time = t
                fps = 60/elapsed
                i = 0;
        self.root.destroy()
