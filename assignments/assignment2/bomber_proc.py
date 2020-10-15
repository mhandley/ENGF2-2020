from tkinter import *
from tkinter import font
from math import sqrt
from random import *
from time import time

#some global constants
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 700
SPACING = 100
speed = 0.0

''' update_position takes a list of x and y coordinates and pair of offsets.
    It creates a new list of x and y coordintes by adding the offsets to all
    the coordinates from the original list '''    

def update_position(position_list, x_offset, y_offset):
    newlist = []
    is_x = True;
    for val in position_list:
        if is_x:
            newlist.append(val + x_offset)
        else:
            newlist.append(val + y_offset)
        is_x = not is_x
    return newlist


''' init_building is called to initialize the state associated with
    one building, and draw it on the canvas.  It takes four lists as
    parameters and appends the relevant state to these lists'''  
def init_building(canvas, building_num, building_width, building_heights, building_xpos, building_rects):
    global rand
    height = rand.randint(10,500) #random number between 10 and 500
    building_heights.append(height)
    x = building_num*SPACING
    building_xpos.append(x)
    building_rects.append(canvas.create_rectangle(x, CANVAS_HEIGHT, x + building_width,
                                                  CANVAS_HEIGHT-height, fill="brown"))

''' is_inside_builing tests if point pos is inside building number
    building_num.  It takes the lists of building widths, heights and x
    positions as parameters '''
def is_inside_building(building_num, pos, building_width, building_heights, building_xpos):
    if (pos[0] < building_xpos[building_num]
        or pos[0] > building_xpos[building_num] + building_width
        or pos[1] < CANVAS_HEIGHT - building_heights[building_num]):
            return False
    return True

''' shrink_building shrinks building number building_num when a bomb drops on it '''
def shrink_building(canvas, building_num, building_width, building_heights, building_xpos, building_rects):
    building_heights[building_num] = building_heights[building_num] - 50
    canvas.delete(building_rects[building_num])
    x = building_xpos[building_num]
    building_rects[building_num] = canvas.create_rectangle(x, CANVAS_HEIGHT, x + building_width,
                                                           CANVAS_HEIGHT-building_heights[building_num], fill="brown")

''' delete building number building_num from the canvas '''
def delete_building(canvas, building_num, building_rects):
    canvas.delete(building_rects[building_num])

''' initialize the state for the bomb.  As there's only one bomb, we store this 
    state as global variables.  One the bomb explodes it can be reused again. '''
def init_bomb(canvas, bomb_pos):
    global bomb_falling, bomb_drawn, bomb_points
    bomb_falling = False
    bomb_drawn = False
    ''' bomb_pos is a two element list holding the bomb's current position '''
    bomb_pos[0] = 0
    bomb_pos[1] = 0
    ''' bomb_points contains x,y coordinate pairs to draw a bomb with top left
        corner at position 0,0'''
    bomb_points = [0,0, 10,0, 5,5, 10,10, 10,20, 5,22, 0,20, 0,10, 5,5]
    draw_bomb(canvas, bomb_pos)

''' draw the bomb at position pos '''
def draw_bomb(canvas, pos):
    global bomb_drawn, bomb_polygon
    current_points = update_position(bomb_points, pos[0], pos[1])
    bomb_polygon = canvas.create_polygon(*current_points, fill="black")
    bomb_drawn = True

''' erase the old bomb, and redraw it at position pos '''
def redraw_bomb(canvas, pos):
    global bomb_drawn, bomb_polygon, bomb_falling
    if bomb_drawn:
        canvas.delete(bomb_polygon)
    if bomb_falling:
        draw_bomb(canvas, pos)

def move_bomb(pos):
    global bomb_falling
    if bomb_falling:
        pos[1] = pos[1] + 8 * speed

''' drop the bomb from the plane at position plane_pos '''
def drop_bomb(pos, plane_pos):
    global bomb_falling
    if bomb_falling:
        # don't drop again while bomb is still falling
        return
    bomb_falling = True
    pos[0] = plane_pos[0]
    pos[1] = plane_pos[1]

def explode():
    global bomb_falling
    bomb_falling = False

''' initialize the state for the plane.  As there's only one plane, we store this 
    state as global variables. '''
def init_plane(canvas, plane_pos):
    global plane_start_x, plane_start_y
    global plane_body_points, plane_wing1_points, plane_wing2_points, plane_tail_points
    global plane_width
    plane_start_x = plane_pos[0]
    plane_start_y = plane_pos[1]
    ''' plane is drawn as four polygons.  The following four lists
        contains x,y coordinate pairs to draw a plane with top
        left corner at position 0,0 '''
    plane_body_points = [0,28, 20,16, 120,16, 94,32, 12,32]
    plane_wing1_points = [40,28, 76,28, 94,48, 80,48]
    plane_wing2_points = [52,16, 78,8, 94,8, 81,16]
    plane_tail_points = [90,16, 110,0, 124,0, 116,16]
    plane_width = 124
    draw_plane(canvas, plane_pos)

''' reset the plane to its starting position at the start of a new level '''
def reset_plane_position(plane_pos):
    plane_pos[0] = plane_start_x
    plane_pos[1] = plane_start_y

def draw_plane(canvas, plane_pos):
    global plane_body_points, plane_wing1_points, plane_wing2_points, plane_tail_points
    global plane_body, plane_wing1, plane_wing2, plane_tail
    x = plane_pos[0]
    y = plane_pos[1]
    current_body_points = update_position(plane_body_points, x, y)
    current_wing1_points = update_position(plane_wing1_points, x, y)
    current_wing2_points = update_position(plane_wing2_points, x, y)
    current_tail_points = update_position(plane_tail_points, x, y)
    plane_body = canvas.create_polygon(*current_body_points, fill="red")
    plane_wing1 = canvas.create_polygon(*current_wing1_points, fill="grey")
    plane_wing2 = canvas.create_polygon(*current_wing2_points, fill="grey")
    plane_tail = canvas.create_polygon(*current_tail_points, fill="grey")

def redraw_plane(canvas, plane_pos):
    global plane_body, plane_wing1, plane_wing2, plane_tail
    canvas.delete(plane_body)
    canvas.delete(plane_wing1)
    canvas.delete(plane_wing2)
    canvas.delete(plane_tail)
    draw_plane(canvas, plane_pos)

''' move the plane however much it moves during one frame '''
def move_plane(pos):
    #position is a two element list: [x,y]
    pos[0] = pos[0] - 4 * speed
    if pos[0] < -plane_width:
        pos[0] += CANVAS_WIDTH
        pos[1] = pos[1] + 40
        #check we don't go off the bottom of the screen
        if pos[1] > CANVAS_HEIGHT:
            pos[1] = CANVAS_HEIGHT
        #we get 10 points each row the plane moves down
        return 10
    else:
        return 0

''' initialize the GUI state and the game state '''    
def init_display(root, plane_pos, bomb_pos, building_heights, building_xpos, building_rects):
    global building_width, game_running, canvas, won
    root.wm_title("Bomber")
    windowsystem = root.call('tk', 'windowingsystem')
    canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
    canvas.pack(side = LEFT, fill=BOTH, expand=FALSE)
    init_fonts()
    init_score(canvas)

    #create game objects
    plane_pos[0] = CANVAS_WIDTH - 100
    plane_pos[1] = 0
    init_plane(canvas, plane_pos)
    init_bomb(canvas, bomb_pos)
    building_width = SPACING * 0.8
    create_buildings(canvas, building_width, building_heights, building_xpos, building_rects)
    game_running = True
    won = False
    return canvas

def init_fonts():
    global bigfont, scorefont
    bigfont = font.nametofont("TkDefaultFont")
    bigfont.configure(size=48)
    scorefont = font.nametofont("TkDefaultFont")
    scorefont.configure(size=20)

def init_score(canvas):
    global score, level, score_text, scorefont
    score = 0
    level = 1
    score_text = canvas.create_text(5, 5, anchor="nw")
    canvas.itemconfig(score_text, text="Score:", font=scorefont)

def display_score(canvas, score, level):
    global score_text, scorefont
    canvas.itemconfig(score_text, text="Level: " + str(level) + "  Score: " + str(score), font=scorefont)

''' create new buildings at the start of a level '''
def create_buildings(canvas, building_width, building_heights, building_xpos, building_rects):
    #remove any old buildings
    if len(building_rects) > 0:
        for building_num in range(0, 1200//SPACING):
            delete_building(canvas, building_num, building_rects)
    building_heights.clear()
    building_xpos.clear()

    #create the new ones
    for building_num in range(0, 1200//SPACING):
        init_building(canvas, building_num, building_width, building_heights, building_xpos, building_rects)

''' check the state of the bomb each frame '''
def check_bomb(canvas, bomb_pos, building_width, building_heights, building_xpos, building_rects):
    if not bomb_falling:
        return
    # did the bomb hit a building?
    for building_num in range(0, 1200//SPACING):
        if is_inside_building(building_num, bomb_pos, building_width, building_heights, building_xpos):
            explode()
            shrink_building(canvas, building_num, building_width, building_heights, building_xpos, building_rects)
    

''' check the state of the plane each frame '''
def check_plane(canvas, plane_pos, building_width, building_heights, building_xpos):
    # we'll check if the plane nose hits a building, or if the
    # base of the fuselage hits.  Won't worry if the wing hits though.
    plane_nose_pos = [plane_pos[0], plane_pos[1] + 28]
    plane_body_pos = [plane_pos[0] + 12, plane_pos[1] + 32]
    plane_wing_pos = [plane_pos[0] + 94, plane_pos[1] + 48]
    for building_num in range(0, 1200//SPACING):
        if (is_inside_building(building_num, plane_nose_pos, building_width,
                               building_heights, building_xpos)
            or is_inside_building(building_num, plane_body_pos, building_width,
                                  building_heights, building_xpos)
            or is_inside_building(building_num, plane_wing_pos, building_width,
                                  building_heights, building_xpos)) :
            game_over(canvas)
    if plane_body_pos[1] == CANVAS_HEIGHT and plane_body_pos[0] < 20:
        plane_landed(canvas)

''' game_over is called when the plane crashes to stop play and display the
    game over message '''
def game_over(canvas):
    global game_running, won, msg_text, bigfont
    game_running = False
    won = False
    msg_text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, anchor="c")
    canvas.itemconfig(msg_text, text="GAME OVER!", font=bigfont)

''' plane_landed is called when the plane has landed to stop plane and
    display the success message '''
def plane_landed(canvas):
    global game_running, won, score, level, msg_text, msg_text2, bigfont, scorefont
    game_running = False
    won = True
    score = score + 1000
    display_score(canvas, score, level)
    msg_text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, anchor="c")
    canvas.itemconfig(msg_text, text="SUCCESS!", font=bigfont)
    msg_text2 = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2 + 100, anchor="c")
    canvas.itemconfig(msg_text2, text="Press n for next level.", font=scorefont)

''' restart is called after game over to start a new game '''
def restart(canvas, plane_pos, building_heights,
            building_xpos, building_rects):
    global building_width, won, game_running, plane, msg_text
    canvas.delete(msg_text)
    level = 1
    score = 0
    reset_plane_position(plane_pos)
    building_width = SPACING * 0.8
    create_buildings(canvas, building_width, building_heights,
                     building_xpos, building_rects)
    won = False
    game_running = True
    return (score, level)

def next_level(canvas, level, plane_pos,
               building_heights, building_xpos, building_rects):
    global building_width, won, game_running
    #don't move to next level unless we've actually won!
    if won == False:
        return level
        
    level = level + 1
    canvas.delete(msg_text)
    canvas.delete(msg_text2)
    reset_plane_position(plane_pos)
    # buildings get narrower with each level 
    building_width = building_width * 0.9
    create_buildings(canvas, building_width, building_heights, building_xpos, building_rects)
    won = False
    game_running = True
    return level

''' key is called by tkinter whenever a key is pressed '''
def key(event):
    global ev, seen_event
    seen_event = True
    ev = event

''' adjust game speed so it's more or less the same on different machines '''
def checkspeed():
    global speed, lastframe, framecount
    framecount = framecount + 1
    # only check every ten frames                                                             
    if framecount == 10:
        now = time()
        elapsed = now - lastframe
        # speed will be 1.0 if we're achieving 60 fps
        if speed == 0:
            #initial speed value                                                              
            # At 60fps, 10 frames take 1/6 of a second.                                       
            speed = 6 * elapsed
        else:
            # use an EWMA to damp speed changes and avoid excessive jitter
            speed = speed * 0.9 + 0.1 * 6 * elapsed
        lastframe = now
        framecount = 0

''' run the main loop of the game '''
def run_game():
    global seen_event, ev, rand, game_running, lastframe, framecount
    root = Tk();
    rand = Random()
    windowsystem = root.call('tk', 'windowingsystem')
    plane_pos = [0, 0] 
    bomb_pos = [0, 0]
    building_heights = []
    building_xpos = []
    building_rects = []
    canvas = init_display(root, plane_pos, bomb_pos, building_heights, building_xpos, building_rects)
    root.bind_all('<Key>', key)
    prog_running = True
    score = 0
    level = 1
    seen_event = False
    lastframe = time()
    framecount = 0
    while prog_running:
        if seen_event:
            if ev.char == ' ':
                drop_bomb(bomb_pos, plane_pos)
            elif ev.char == 'q':
                prog_running = False
            elif ev.char == 'n':
                level = next_level(canvas, level, plane_pos, building_heights,
                                   building_xpos, building_rects)
            elif ev.char == 'r':
                (score, level) = restart(canvas, plane_pos, building_heights,
                                         building_xpos, building_rects)
            seen_event = False
            
        if game_running:
            score = score + move_plane(plane_pos)
            check_plane(canvas, plane_pos, building_width, building_heights, building_xpos)
            move_bomb(bomb_pos)
            check_bomb(canvas, bomb_pos, building_width, building_heights, building_xpos, building_rects)
            redraw_plane(canvas, plane_pos)
            redraw_bomb(canvas, bomb_pos)
            display_score(canvas, score, level)
        root.update()
        checkspeed()
    root.destroy()

run_game()
