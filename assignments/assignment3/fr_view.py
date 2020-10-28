# Simple Frogger Game.  Mark Handley, UCL, 2018

from tkinter import *
from tkinter import font
import time
from fr_settings import CANVAS_WIDTH, CANVAS_HEIGHT, GRID_SIZE, LOG_HEIGHT, Direction

'''GameObjectView is a generic view of a game object.  All it does is
   handle moving of the object - it just saves replicating this code into
   LogView, CarView, etc.  Everything else needs to be handled by the
   subclasses themselves.'''

class GameObjectView():
    def __init__(self, canvas):
        self.canvas = canvas
        self.items = []
        self.x = 0
        self.y = 0

    def moveto(self, x, y):
        for item in self.items:
            self.canvas.move(item, x - self.x, y - self.y)
        self.x = x
        self.y = y

    def cleanup(self):
        for item in self.items:
            self.canvas.delete(item)

    
class LogView(GameObjectView):
    def __init__(self, canvas, log):
        GameObjectView.__init__(self, canvas)
        self.log = log
        width = log.get_width()
        #y_offset centres the log vertically in the grid squares
        #logs are vertically centered about the y value from their model
        y_offset = (GRID_SIZE - LOG_HEIGHT) // 2 - GRID_SIZE/2
        rect = self.canvas.create_rectangle(10, y_offset, width-10, LOG_HEIGHT + y_offset, fill="brown", outline="brown")
        circle = self.canvas.create_oval(0, y_offset, 20, LOG_HEIGHT + y_offset, fill="brown", outline="white")
        circle2 = self.canvas.create_oval(width-20, y_offset, width, LOG_HEIGHT + y_offset, fill="brown", outline="brown")
        self.items.append(rect)
        self.items.append(circle)
        self.items.append(circle2)

    def redraw(self, time_now):
        (x,y) = self.log.get_position()
        self.moveto(x, y)

class TurtleView(GameObjectView):
    def __init__(self, canvas, turtle, pngs):
        GameObjectView.__init__(self, canvas)
        self.turtle = turtle
        self.pngs = pngs
        self.pngnum = 0
        self.last_change = time.time()
        self.draw()

    def draw(self):
        width = self.turtle.get_width()
        self.pngnum = 1 - self.pngnum #alternate images
        (x,y) = self.turtle.get_position()
        self.moveto(0, 0)
        for i in range(0, width//GRID_SIZE):
            image = self.canvas.create_image(i * GRID_SIZE, 0, image=self.pngs[self.pngnum], anchor="c")
            self.items.append(image)
        self.moveto(x, y)

    def redraw(self, time_now):
        width = self.turtle.get_width()
        (x,y) = self.turtle.get_position()
        if time_now - self.last_change < 0.2:
            for i in range(0, width//GRID_SIZE):
                self.moveto(x, y)
        else:
            for img in self.items:
                self.canvas.delete(img)
            self.items.clear()
            self.draw()
            self.last_change = time_now

class CarView(GameObjectView):
    def __init__(self, canvas, car, png):
        GameObjectView.__init__(self, canvas)
        self.car = car
        image = canvas.create_image(0, 0, image=png, anchor="c")
        self.items.append(image)

    def redraw(self):
        (x,y) = self.car.get_position()
        self.moveto(x, y)
            

''' Dummy frog model, for frogs in home, or uses as lives remaining '''
class DummyFrog():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = Direction.UP
        self.moving = False

    def get_position(self):
        return (self.x, self.y)
            
    def get_direction(self):
        return self.direction


class FrogView(GameObjectView):
    def __init__(self, canvas, frog, pngs):
        GameObjectView.__init__(self, canvas)
        self.frog = frog
        self.pngs = pngs
        self.dead = False
        self.draw()

    def draw(self):
        (x, y) = self.frog.get_position()
        self.dir = self.frog.get_direction()
        if self.dead:
            img = self.pngs[len(self.pngs)-1] #the death image is at the end of the list
        elif self.frog.moving:
            # if the frog is jumping, use the alternative images
            img = self.pngs[self.dir.value + 4]
        else:
            img = self.pngs[self.dir.value]
        self.moveto(x, y)
        frogimage = self.canvas.create_image(x, y, image=img, anchor="c")
        self.canvas.tag_raise(frogimage)
        self.items.append(frogimage)

    def redraw(self, time_now):
        if self.dead:
            self.check_undead(time_now)
        self.canvas.delete(self.items[0])
        self.items.clear()
        self.draw()

    def died(self):
        self.dead = True
        self.died_time = time.time()
        self.canvas.delete(self.items[0])
        self.items.clear()
        self.draw()

    def check_undead(self, time_now):
        if time_now - self.died_time < 1:
            #still dead
            return
        self.dead = False
        self.canvas.delete(self.items[0])
        self.items.clear()
        self.draw()


class TimeView():
    def __init__(self, canvas):
        self.canvas = canvas
        self.end_time = time.time()
        self.bar = self.canvas.create_rectangle(0,0,0,0) #placeholder

    def reset(self, end_time):
        self.end_time = end_time

    def update(self, time_now):
        remaining = self.end_time - time_now
        if remaining > 0:
            self.canvas.delete(self.bar)
            self.bar = self.canvas.create_rectangle(CANVAS_WIDTH - 20*remaining - 100, GRID_SIZE*16.25,
                                               CANVAS_WIDTH - 100, GRID_SIZE*16.75, fill="green")

            
class View(Frame):
    def __init__(self, root, controller):
        self.controller = controller
        root.wm_title("Frogger")
        self.windowsystem = root.call('tk', 'windowingsystem')
        self.frame = root
        self.canvas = Canvas(self.frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
        self.canvas.pack(side = LEFT, fill=BOTH, expand=FALSE)
        self.init_fonts()
        self.init_score()
        self.messages_displayed = False
        self.river_views = []
        self.car_views = []
        self.lives = 0
        self.lives_frogs = []
        self.home_frogs = []
        self.timer = TimeView(self.canvas)

        #Load all the images from files
        self.frog_pngs = []
        for i in range(1, 10):
            try:
                self.frog_pngs.append(PhotoImage(file = './frog' + str(i) + '.png').zoom(2))
            except:
                self.frog_pngs.append(PhotoImage(file = './frog' + str(i) + '.gif').zoom(2))
        self.car_pngs = []
        for i in range(1, 5):
            try:
                self.car_pngs.append(PhotoImage(file = './car' + str(i) + '.png').zoom(2))
            except:
                self.car_pngs.append(PhotoImage(file = './car' + str(i) + '.gif').zoom(2))
        self.turtle_pngs = []
        for i in range(1, 3):
            try:
                self.turtle_pngs.append(PhotoImage(file = './turtle' + str(i) + '.png').zoom(2))
            except:
                self.turtle_pngs.append(PhotoImage(file = './turtle' + str(i) + '.gif').zoom(2))

        self.init_scenery()

    def init_scenery(self):
        # the game objects are aligned so their vertical centres are
        # on the grid boundaries, so the scenery needs to be offset by
        # half a square
        yoff = GRID_SIZE//2 
        self.canvas.create_rectangle(0,GRID_SIZE*3 - yoff, CANVAS_WIDTH, GRID_SIZE*9 - yoff, fill="darkblue")
        self.canvas.create_rectangle(0,GRID_SIZE*9 - yoff, CANVAS_WIDTH, GRID_SIZE*10 - yoff, fill="purple")
        self.canvas.create_rectangle(0,GRID_SIZE*15 - yoff, CANVAS_WIDTH, GRID_SIZE*16 - yoff, fill="purple")

        #create the frog homes at the top of the screen
        self.canvas.create_rectangle(0,GRID_SIZE*2.5 - yoff, CANVAS_WIDTH, GRID_SIZE*3 - yoff, fill="green", outline="green")
        spacing = (CANVAS_WIDTH - GRID_SIZE*5)//5
        x = -spacing//2
        for i in range(0,6):
            self.canvas.create_rectangle(x,GRID_SIZE*3 - yoff, x + spacing, GRID_SIZE*4 - yoff, fill="green", outline="green")
            x = x + GRID_SIZE + spacing
            
    def init_fonts(self):
        self.bigfont = font.nametofont("TkDefaultFont")
        self.bigfont.configure(size=48)
        self.scorefont = font.nametofont("TkDefaultFont")
        self.scorefont.configure(size=20)

    def init_score(self):
        self.score_text = self.canvas.create_text(5, 5, anchor="nw")
        self.canvas.itemconfig(self.score_text, text="Score:", font=self.scorefont, fill="white")
        self.time_text = self.canvas.create_text(CANVAS_WIDTH, GRID_SIZE*16, anchor="ne")
        self.canvas.itemconfig(self.time_text, text="TIME", font=self.scorefont, fill="yellow")

    def register_frog(self, frog_model):
        self.frog_view = FrogView(self.canvas, frog_model, self.frog_pngs)

    def register_car(self, car_model):
        carnum = car_model.get_carnum()
        self.car_views.append(CarView(self.canvas, car_model, self.car_pngs[carnum]))

    def register_river_object(self, model):
        if model.is_log():
            self.river_views.append(LogView(self.canvas, model))
        else:
            pngs = self.turtle_pngs
            self.river_views.append(TurtleView(self.canvas, model, pngs))

    def unregister_objects(self):
        for view in self.river_views:
            view.cleanup()
        self.river_views.clear()
        for car_view in self.car_views:
            car_view.cleanup()
        self.car_views.clear()

    def display_score(self):
        self.canvas.itemconfig(self.score_text, text="Level: " + str(self.controller.get_level())
                               + "  Score: " + str(self.controller.get_score()), font=self.scorefont)
        self.update_lives()

    def update_lives(self):
        lives = self.controller.get_lives()
        if lives != self.lives:
            self.lives = lives
            for frog_view in self.lives_frogs:
                frog_view.cleanup()
            self.lives_frogs.clear()
            y = GRID_SIZE * 16  # 16 rows down is where we show the lives remaining
            for i in range(0, self.lives - 1):
                x = GRID_SIZE * (i + 1)
                dummy = DummyFrog(x, y)
                self.lives_frogs.append(FrogView(self.canvas, dummy, self.frog_pngs))

    ''' a frog has reached home '''
    def frog_is_home(self, x, y):
        dummy = DummyFrog(x, y)
        self.home_frogs.append(FrogView(self.canvas, dummy, self.frog_pngs))

    def died(self):
        self.frog_view.died()

    def reset_level(self, end_time):
        for frog_view in self.home_frogs:
            frog_view.cleanup()
        self.home_frogs.clear()
        self.clear_messages()
        self.timer.reset(end_time)

    def game_over(self):
        self.text = self.canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2 + 10, anchor="c")
        self.canvas.itemconfig(self.text, text="GAME OVER!", font=self.bigfont,
                               fill="white")
        self.text2 = self.canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2 + 110, anchor="c")
        self.canvas.itemconfig(self.text2, text="Press r to play again.", font=self.scorefont,
                               fill="white")
        self.messages_displayed = True

    def clear_messages(self):
        if self.messages_displayed:
            self.canvas.delete(self.text)
            self.canvas.delete(self.text2)
            self.messages_displayed = False

    def update(self):
        now = time.time()
        for view in self.river_views:
            view.redraw(now)
        for car_view in self.car_views:
            car_view.redraw()
        self.display_score()
        self.timer.update(now)
        self.frog_view.redraw(now)

