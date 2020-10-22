from time import sleep
from fr_model import Model, RiverObject, Frog, Car, Log, speed
from fr_settings import CANVAS_WIDTH, CANVAS_HEIGHT, GRID_SIZE, LOG_HEIGHT, Direction, GRID_SIZE

class DummyController():
    def __init__(self):
        self.frog = None
        self.score = -1
        self.level = -1
        self.end_time = 0
        self.lives = 0
        self.river_objects = []
        self.cars = []

    def register_frog(self, frog):
        self.frog = frog

    def update_score(self, score):
        self.score = score

    def update_level(self, level, end_time):
        self.level = level
        self.end_time = end_time

    def update_lives(self, lives):
        self.lives = lives

    def register_river_object(self, obj):
        self.river_objects.append(obj)

    def register_car(self, obj):
        self.cars.append(obj)

    def died(self):
        assert(True)  # just a placeholder

def test_river_object():
    global speed
    x = 100
    y = 100
    width = 200
    obj_speed = 10
    r_obj1 = RiverObject(x, y,width,Direction.RIGHT,obj_speed)
    assert(r_obj1.get_position() == (x, y))
    assert(r_obj1.get_width() == width)

    # test object moves as expected to right
    assert(speed == 1.0) # test assumes this is 1.0
    r_obj1.move()
    assert(r_obj1.get_position() == (x+obj_speed, y))

    # test object moves as expected to left
    r_obj2 = RiverObject(x, y,width,Direction.LEFT,obj_speed)
    r_obj2.move()
    assert(r_obj2.get_position() == (x-obj_speed, y))

    # check the object wraps from left to right properly
    x1 = -CANVAS_WIDTH//2 + 1.5 * obj_speed
    r_obj4 = RiverObject(x1, y,width,Direction.LEFT,obj_speed)
    assert(r_obj4.get_position() == (x1, y))
    r_obj4.move()
    assert(r_obj4.get_position() == (x1-obj_speed, y))
    r_obj4.move()
    assert(r_obj4.get_position() == (CANVAS_WIDTH, y))

    #check contains function
    r_obj3 = RiverObject(x, y,width,Direction.LEFT,obj_speed)
    frog1 = Frog(99,100)
    frog2 = Frog(200,100)
    frog3 = Frog(301,100)
    frog4 = Frog(200,90)
    assert(not r_obj3.contains(frog1))
    assert(r_obj3.contains(frog2))
    assert(not r_obj3.contains(frog3))
    assert(not r_obj3.contains(frog4))

def test_car():
    x = 100
    y = 100
    car_speed = 10
    carnum = 1
    car1 = Car(x, y, carnum, Direction.LEFT, car_speed)
    assert(car1.get_position() == (x,y))
    car1.move()
    assert(car1.get_position() == (x-car_speed, y))

    car2 = Car(x, y, carnum, Direction.RIGHT, car_speed)
    assert(car2.get_position() == (x,y))
    car2.move()
    assert(car2.get_position() == (x+car_speed, y))
    
    x1 = -CANVAS_WIDTH//2 + 1.5 * car_speed
    car3 = Car(x1, y,carnum,Direction.LEFT,car_speed)
    assert(car3.get_position() == (x1, y))
    car3.move()
    assert(car3.get_position() == (x1-car_speed, y))
    car3.move()
    assert(car3.get_position() == (CANVAS_WIDTH, y))
    
    car4 = Car(x, y, carnum, Direction.LEFT, car_speed)
    assert(car4.collided(x, y))
    assert(not car4.collided(x, y-1))
    assert(not car4.collided(x, y+1))
    assert(not car4.collided(x-GRID_SIZE, y))
    assert(car4.collided(x-GRID_SIZE//2, y))
    assert(not car4.collided(x+GRID_SIZE, y))
    assert(car4.collided(x+GRID_SIZE//2, y))

def test_frog():
    x = 100
    y = 100
    frog = Frog(100,100)
    assert(frog.get_position() == (x, y))
    assert(frog.get_direction() == Direction.UP)
    assert(frog.on_log() == None)

    frog.move(Direction.UP)
    frog.finish_move()
    assert(frog.get_position() == (x, y - GRID_SIZE//2))
    sleep(0.2)
    frog.finish_move()
    assert(frog.get_position() == (x, y - GRID_SIZE))

    frog.move(Direction.LEFT)
    sleep(0.2)
    frog.finish_move()
    assert(frog.get_position() == (x - GRID_SIZE, y - GRID_SIZE))

    frog.move(Direction.DOWN)
    sleep(0.2)
    frog.finish_move()
    frog.move(Direction.RIGHT)
    sleep(0.2)
    frog.finish_move()
    assert(frog.get_position() == (x, y))

    frog.move(Direction.DOWN)
    sleep(0.2)
    frog.finish_move()
    assert(frog.get_position() == (x, y + GRID_SIZE))
    frog.reset_position()
    assert(frog.get_position() == (x, y))

    #test moving with log
    lx = 80
    ly = 100
    lwidth = 40  #short log!
    lspeed = 10
    log = Log(lx, ly, lwidth, Direction.RIGHT, lspeed)
    assert(log.contains(frog))

    frog.move_with(log)
    assert(frog.get_position() == (x, y))
    assert(frog.on_log() == log)

    log.move()
    frog.move_with(log)
    assert(frog.get_position() == (x + lspeed, y))
    log.move()
    frog.move_with(log)
    assert(frog.get_position() == (x + lspeed*2, y))

def unpause_func():  #used to test unpause callback
    global paused
    paused = False
    
def test_model_pause():
    controller = DummyController()
    model = Model(controller)
    model.dummyvar = 0  # use this to test the callback was called correctly
    model.pause_start(0.1, "self.dummyvar=1")
    assert(model.paused)
    model.check_pause()
    assert(model.paused)
    assert(model.dummyvar==0)
    sleep(0.2)
    model.check_pause()
    assert(not model.paused)
    assert(model.dummyvar==1)

    
def test_model():
    controller = DummyController()
    assert(controller.frog == None)
    
    model = Model(controller)
    assert(controller.frog != None)
    assert(controller.score == 0)
    assert(controller.level == 1)

    # check model.update() moves the frog properly
    (fx, fy) = controller.frog.get_position()
    model.move_frog(Direction.LEFT)
    model.update()
    sleep(0.2)
    model.update()
    assert(controller.frog.get_position() == (fx - GRID_SIZE, fy))

    # check model.update() moves the frog properly
    model.move_frog(Direction.RIGHT)
    model.update()
    sleep(0.2)
    model.update()
    assert(controller.frog.get_position() == (fx, fy))


    # test check_frog()
    # test that the frog correctly dies when moving off the left side
    lives = model.lives
    assert(lives > 1)
    controller.frog.x = GRID_SIZE  #just on the left side of the screen

    model.move_frog(Direction.LEFT)
    model.update()
    sleep(0.2)
    model.update()
    model.check_frog()
    assert(controller.frog.get_position() == (0, fy))
    assert(lives == model.lives)   # we didn't die yet

    model.move_frog(Direction.LEFT)
    model.update()
    sleep(0.2)
    model.update()
    model.check_frog()
    assert(lives -1 == model.lives)   # we died by moving off the left

    sleep(1.2) # wait for restart (happens 1 sec after dying)
    assert(controller.frog.get_position() != (fx, fy)) #check frog is not back in starting position
    model.check_pause()  # finish the post-dead pause
    assert(controller.frog.get_position() == (fx, fy)) #check frog is back in starting position

    # test that the frog correctly dies when moving off the right side
    lives = model.lives
    assert(lives > 1)
    controller.frog.x = CANVAS_WIDTH - GRID_SIZE  #just on the right side of the screen
    model.move_frog(Direction.RIGHT)
    model.update()
    sleep(0.2)
    model.update()
    model.check_frog()
    assert(controller.frog.get_position() == (CANVAS_WIDTH, fy))
    assert(lives == model.lives)   # we didn't die yet

    model.move_frog(Direction.RIGHT)
    model.update()
    sleep(0.2)
    model.update()
    model.check_frog()
    assert(lives -1 == model.lives)   # we died by moving off the right
    
    sleep(1.2) # wait for restart (happens 1 sec after dying)
    assert(controller.frog.get_position() != (fx, fy)) #check frog is not back in starting position
    model.check_pause()  # finish the post-dead pause
    assert(controller.frog.get_position() == (fx, fy)) #check frog is back in starting position
    
