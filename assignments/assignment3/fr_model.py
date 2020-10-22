# Simple Frogger Game.  Mark Handley, UCL, 2018-2020

from random import *
import time
from fr_settings import CANVAS_WIDTH, CANVAS_HEIGHT, GRID_SIZE, LOG_HEIGHT, Direction

LEVEL_TIME = 120
speed = 1.0

class RiverObject():
    def __init__(self, x, y, width, dir, speed):
        self.x = x
        self.y = y
        self.width = width
        self.dir = dir
        self.speed = speed

    def get_width(self):
        return self.width

    def get_position(self):
        return (self.x, self.y)

    def move(self):
        global speed
        if self.dir == Direction.RIGHT:
            self.x = self.x + self.speed * speed
            if self.x + self.width > CANVAS_WIDTH * 1.5:
                self.x = -self.width
        else:
            self.x = self.x - self.speed * speed
            if self.x < -0.5 * CANVAS_WIDTH:
                self.x = CANVAS_WIDTH

    def contains(self, frog):
        (frog_x, frog_y) = frog.get_position()
        if frog_y != self.y or frog_x < self.x or frog_x > self.x + self.width:
            return False
        return True

#logs and turtles are both river objects - they move and act mostly the same
class Log(RiverObject):
    def __init__(self, x, y, width, dir, speed):
        RiverObject.__init__(self, x, y, width, dir, speed)

    def is_log(self):
        return True
        
class Turtle(RiverObject):
    def __init__(self, x, y, width, dir, speed):
        RiverObject.__init__(self, x, y, width, dir, speed)
        self.sunk = False

    def is_log(self):
        return False

    def is_sunk(self):
        return self.sunk;
    
        
        
class Car():
    def __init__(self, x, y, carnum, dir, speed):
        self.x = x
        self.y = y
        self.dir = dir
        self.carnum = carnum
        self.speed = speed

    def get_position(self):
        return (self.x, self.y)

    def get_carnum(self):
        return self.carnum

    def move(self):
        global speed
        if self.dir == Direction.RIGHT:
            self.x = self.x + self.speed * speed
            if self.x + GRID_SIZE > CANVAS_WIDTH * 1.5:
                self.x = -GRID_SIZE
        else:
            self.x = self.x - self.speed * speed
            if self.x < -0.5 * CANVAS_WIDTH:
                self.x = CANVAS_WIDTH

    def collided(self, frog_x, frog_y):
        # cars are alligned vertically on same grid as frogs
        if frog_y != self.y:
            return False
        # x positions are center of objects
        # frog doesn't fill a square, so allow some slack
        margin = (GRID_SIZE*8)//10
        if frog_x > self.x - margin and frog_x < self.x + margin:
            return True


class Frog():
    def __init__(self, x, y):
        self.start_position = (x, y)
        self.x = x
        self.y = y
        self.direction = Direction.UP
        self.log = None #we're not on a log yet
        self.moving = False #we're not moving

    def get_position(self):
        return (self.x, self.y)

    def get_direction(self):
        return self.direction

    def reset_position(self):
        (self.x,self.y) = self.start_position

    ''' which log are we on, or None if we're not on a log '''
    def on_log(self):
        return self.log

    ''' we're on a log.  Move along with it. '''
    def move_with(self, log):
        if self.log != log:
            #we've just joined this log
            self.log = log
            (self.log_x, log_y) = log.get_position()
            #no need to move this time
        else:
            (log_x, log_y) = log.get_position()
            x_delta = log_x - self.log_x
            self.x = self.x + x_delta
            self.log_x = log_x
            
    ''' move due to user input '''
    def move(self, dir):
        self.direction = dir
        if self.moving:
            return
        self.moving = True
        self.start_move_time = time.time()
        if dir == Direction.LEFT:
            self.x = self.x - GRID_SIZE//2
        elif dir == Direction.RIGHT:
            self.x = self.x + GRID_SIZE//2
        elif dir == Direction.UP:
            self.y = self.y - GRID_SIZE//2
        elif dir == Direction.DOWN:
            self.y = self.y + GRID_SIZE//2

    def finish_move(self):
        if (not self.moving) or (time.time() - self.start_move_time < 0.1):
            return
        dir = self.direction
        if dir == Direction.LEFT:
            self.x = self.x - GRID_SIZE//2
        elif dir == Direction.RIGHT:
            self.x = self.x + GRID_SIZE//2
        elif dir == Direction.UP:
            self.y = self.y - GRID_SIZE//2
        elif dir == Direction.DOWN:
            self.y = self.y + GRID_SIZE//2
        self.moving = False

class Model():
    def __init__(self, controller):
        self.controller = controller
        self.lives = 7
        self.end_time = time.time() + LEVEL_TIME
        self.init_score()
        self.rand = Random()

        #create game objects
        self.frog = Frog(CANVAS_WIDTH//2, GRID_SIZE*15)
        controller.register_frog(self.frog)
        self.logs = []
        self.cars = []
        self.create_logs()
        self.create_cars()
        self.create_homes()
        self.game_running = True
        self.paused = False
        self.won = False

        # initialized speed measurement (see checkspeed for use)
        self.lastframe = time.time()
        self.framecount = 0
        self.dont_update_speed = True

    def activate(self):
        self.controller.update_score(0)
        self.controller.update_level(self.level, self.end_time)
        self.controller.update_lives(self.lives)

    def init_score(self):
        self.score = 0
        self.level = 1
        self.controller.update_score(0)
        self.controller.update_level(self.level, self.end_time)
        self.controller.update_lives(self.lives)

    def create_logs(self):
        #remove any old logs or turtles
        self.logs.clear()

        #create the new ones
        y = GRID_SIZE*4
        speeds = [1, 1, 2.5, 1, 2]
        turtles = [False, True, False, False, True] # true if this is a turtle
        for row in range(0, 5):
            width = 0
            x = 0
            for log_num in range(0, 5):
                space = self.rand.randint(50,200) + self.level*50
                x = x + width + space
                if x < CANVAS_WIDTH * 1.5:
                    #turtles go left, logs go right
                    if turtles[row]: 
                        dir = Direction.LEFT
                    else:
                        dir = Direction.RIGHT
                    if turtles[row]:
                        # needs to be either two or three turtles long
                        width = self.rand.randint(2,3) * GRID_SIZE 
                        object = Turtle(x, y, width, dir, speeds[row])
                    else:
                        width = self.rand.randint(80,200 - self.level * 20)
                        object = Log(x, y, width, dir, speeds[row])
                    self.logs.append(object);
                    self.controller.register_river_object(object)
            y = y + GRID_SIZE

    def create_cars(self):
        #remove any old cars
        self.cars.clear()

        y = GRID_SIZE*10
        speeds = [2, 4, 2.5, 1, 3]
        carnums = [1, 2, 1, 3, 0]
        for row in range(0, 5):
            x = 0
            for car_num in range(0, 8):
                space = self.rand.randint(50,200)
                x = x + space*speeds[row] + GRID_SIZE
                if x < CANVAS_WIDTH * 1.5:
                    #alternate left and right directions
                    if row % 2 == 0:
                        dir = Direction.LEFT
                    else:
                        dir = Direction.RIGHT
                    carnum = 0
                    car = Car(x, y, carnums[row], dir, speeds[row])
                    self.cars.append(car)
                    self.controller.register_car(car)
            y = y + GRID_SIZE

    def create_homes(self):
        # init where the frog homes are at the top of the screen
        self.frogs_home = 0
        self.homes_x = []
        self.homes_occupied = []
        spacing = (CANVAS_WIDTH - GRID_SIZE*5)//5
        # the left hand home has centre position of spacing/2 (green to
        # the left of the home) + GRID_SIZE/2 (to get the centre of the
        # grid square)
        x = (spacing + GRID_SIZE)//2
        for i in range(0,6):
            x = x + GRID_SIZE + spacing
            self.homes_x.append(x)
            self.homes_occupied.append(False)

    def frog_is_home(self, home_num):
        assert(home_num >= 0 and home_num <= 4)
        self.frogs_home = self.frogs_home + 1
        self.homes_occupied[home_num] = True

        #update score
        self.score = self.score + 200
        remaining_time = int(self.end_time - time.time())
        if remaining_time > 0:
            self.score = self.score + remaining_time

        #update view
        (x, y) = self.frog.get_position()
        self.controller.frog_is_home(x, y)

        if self.frogs_home == 5:
            self.level_finished()
        else:
            self.pause_start(1, "self.frog.reset_position()")

    def level_finished(self):
        self.pause_start(1, "self.next_level()")

    def reset_homes(self):
        for i in range(0,6):
            self.homes_occupied[i] = False

    def died(self):
        self.lives = self.lives - 1
        self.controller.died()
        if self.lives == 0:
            self.game_over()
        else:
            self.pause_start(1, "self.new_life()")

    def pause_start(self, pause_time, unpause_function):
        self.paused = True
        self.pause_end_time = time.time() + pause_time
        # register the function to call when we unpause
        self.unpause_function = unpause_function

    def check_pause(self):
        if time.time() > self.pause_end_time:
            self.paused = False
            self.dont_update_speed = True
            # evaluate the registered function
            exec(self.unpause_function)
            
    def new_life(self):
        self.controller.update_lives(self.lives)

    def game_over(self):
        self.game_running = False
        self.won = False
        self.controller.game_over()

    def restart(self):
        self.level = 1
        self.score = 0
        self.reset_level()
        self.dont_update_speed = True

    def next_level(self):
        self.level = self.level + 1
        self.reset_level()

    def reset_level(self):
        self.frogs_home = 0
        self.end_time = time.time() + LEVEL_TIME
        self.controller.update_level(self.level, self.end_time)
        self.frog.reset_position()
        self.lives = 7
        self.controller.update_lives(self.lives)
        self.reset_homes()
        self.controller.unregister_objects()
        self.create_logs()
        self.create_cars()
        self.won = False
        self.paused = False

    def move_frog(self, dir):
        if self.game_running and not self.paused:
            self.frog.move(dir)

    def move_objects(self):
        for log in self.logs:
            log.move()
        for car in self.cars:
            car.move()

    def check_frog_crossing_river(self):
        # frog is crossing the river
        on_log = self.frog.on_log()
        if (not (on_log is None)) and (not on_log.contains(self.frog)):
            # frog was on a log, but has now left that log
            on_log = None
        if on_log is None:
            # it's no longer on the previous log
            # check if it's now on any other log
            for log in self.logs:
                if log.contains(self.frog):
                    on_long = log
                    break
        if on_log is None:
            # frog is not on a log - it must be in the water
            self.died()
            return
        else:
            # frog is on a log
            self.frog.move_with(on_log)

    def check_frog_crossing_road(self):
        # frog is on the road
        (x, y) = self.frog.get_position()
        for car in self.cars:
            if car.collided(x, y):
                self.died()
                return

    def check_frog_entering_home(self):
        # frog is attempting to enter home
        (x, y) = self.frog.get_position()
        for i in range(0, 5):
            if abs(self.homes_x[i] - x) < GRID_SIZE/2 and not self.homes_occupied[i]:
                #we're in a free home
                self.frog_is_home(i)
                return
        self.died()

    def check_frog(self):
        if self.frog.moving:
            self.frog.finish_move()
            return
        
        (x, y) = self.frog.get_position()
        if x < 0 or x > CANVAS_WIDTH:
            self.died()
            return

        if y >= GRID_SIZE * 10 and y <= GRID_SIZE * 14:
            # frog is on the road
            self.check_frog_crossing_road()
        elif y >= GRID_SIZE * 4 and y <= GRID_SIZE * 8:
            # frog is crossing the river
            self.check_frog_crossing_river()
        elif y == GRID_SIZE * 3:
            # frog is attempting to enter home
            self.check_frog_entering_home()

    ''' adjust game speed so it's more or less the same on different machines '''
    def checkspeed(self):
        global speed
        self.framecount = self.framecount + 1
        # only check every ten frames                                                        
        if self.framecount == 10:
            now = time.time()
            elapsed = now - self.lastframe
            self.lastframe = now
            self.framecount = 0
            # if we've just started, or just unpaused, don't update
            # the speed as it will end up wrong
            if self.dont_update_speed == True:
                self.dont_update_speed = False  
                return
            # speed will be 1.0 if we're achieving 60 fps                                    
            if speed == 0:
                #initial speed value                                                         
		# At 60fps, 10 frames take 1/6 of a second.                                  
                speed = 6 * elapsed
            else:
                # use an EWMA to damp speed changes and avoid excessive jitter               
                speed = speed * 0.9 + 0.1 * 6 * elapsed
        
    def update(self):
        if self.game_running and not self.paused:
            self.move_objects()
            self.controller.update_score(self.score)
            self.check_frog()
            self.checkspeed()
        elif self.paused:
            self.check_pause()

