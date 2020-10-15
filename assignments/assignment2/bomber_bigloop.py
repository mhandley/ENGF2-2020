from tkinter import *
from tkinter import font
from math import sqrt
from random import *
from time import time

# some global constants
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 700
SPACING = 100

''' key is called by tkinter whenever a key is pressed '''
def key(event):
    global ev, seen_event
    seen_event = True
    ev = event

''' initialize tkinter and the graphics canvas '''
root = Tk();
rand = Random()
windowsystem = root.call('tk', 'windowingsystem')

#create a window and a canvas
root.wm_title("Bomber")
windowsystem = root.call('tk', 'windowingsystem')
canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
canvas.pack(side = LEFT, fill=BOTH, expand=FALSE)

#initialize some fonts
bigfont = font.nametofont("TkDefaultFont")
bigfont.configure(size=48)
scorefont = font.nametofont("TkDefaultFont")
scorefont.configure(size=20)

#initialize the scoreboard
score = 0
level = 1
score_text = canvas.create_text(5, 5, anchor="nw")
canvas.itemconfig(score_text, text="Score:", font=scorefont)

#create game objects
#plane
plane_x = CANVAS_WIDTH - 100
plane_y = 0
plane_start_x = plane_x
plane_start_y = plane_y
''' plane is drawn as four polygons.  The following four lists                      
    contain x,y coordinate pairs to draw a plane with top                          
    left corner at position 0,0 '''
plane_body_points = [0,28, 20,16, 120,16, 94,32, 12,32]
plane_wing1_points = [40,28, 76,28, 94,48, 80,48]
plane_wing2_points = [52,16, 78,8, 94,8, 81,16]
plane_tail_points = [90,16, 110,0, 124,0, 116,16]
plane_width = 124
plane_body = canvas.create_polygon(*plane_body_points, fill="red")
plane_wing1 = canvas.create_polygon(*plane_wing1_points, fill="grey")
plane_wing2 = canvas.create_polygon(*plane_wing2_points, fill="grey")
plane_tail = canvas.create_polygon(*plane_tail_points, fill="grey")

#create the state associated with the bomb, and draw it on the canvas
bomb_falling = False
bomb_drawn = False
bomb_x = 0
bomb_y = 0
''' bomb_points contains x,y coordinate pairs to draw a bomb with top left              
    corner at position 0,0'''
bomb_points = [0,0, 10,0, 5,5, 10,10, 10,20, 5,22, 0,20, 0,10, 5,5]
bomb_polygon = canvas.create_polygon(*bomb_points, fill="black")
bomb_drawn = True

#create the state associated with the buildings, and draw them on the canvas
building_heights = []
building_xpos = []
building_rects = []
building_width = SPACING * 0.8
for building_num in range(0, 1200//SPACING):
    height = rand.randint(10,500) #random number between 10 and 500
    building_heights.append(height)
    x = building_num*SPACING
    building_xpos.append(x)
    building_rects.append(canvas.create_rectangle(x, CANVAS_HEIGHT, x + building_width,
                                                  CANVAS_HEIGHT-height, fill="brown"))

#set key binding from GUI
root.bind_all('<Key>', key)

prog_running = True
game_running = True
won = False
score = 0
level = 1
seen_event = False
speed = 0.0
lastframe = time()
framecount = 0
while prog_running:
    if seen_event:
        rebuild_buildings = False
        if ev.char == ' ':
            # don't drop again while bomb is still falling
            if not bomb_falling:
                bomb_falling = True
                bomb_x = plane_x
                bomb_y = plane_y
        elif ev.char == 'q':
            prog_running = False
        elif ev.char == 'n':
            # move to the next level
            if won != False:
                level = level + 1
                canvas.delete(msg_text)
                canvas.delete(msg_text2)
                plane_x = plane_start_x
                plane_y = plane_start_y
                # buildings get narrower with each level 
                building_width = building_width * 0.9
                rebuild_buildings = True
                won = False
                game_running = True
        elif ev.char == 'r':
            # restart the game
            canvas.delete(msg_text)
            level = 1
            score = 0
            plane_x = plane_start_x
            plane_y = plane_start_y
            building_width = SPACING * 0.8
            rebuild_buildings = True
            won = False
            game_running = True
        seen_event = False

        if rebuild_buildings:
            # we start a new level, so must rebuild the buildings
            # remove any old buildings
            if len(building_rects) > 0:
                for building_num in range(0, 1200//SPACING):
                    canvas.delete(building_rects[building_num])
            building_rects.clear()
            building_heights.clear()
            building_xpos.clear()

            # create the new ones
            for building_num in range(0, 1200//SPACING):
                height = rand.randint(10,500) #random number between 10 and 500
                building_heights.append(height)
                x = building_num*SPACING
                building_xpos.append(x)
                building_rects.append(canvas.create_rectangle(x, CANVAS_HEIGHT, x + building_width,
                                                              CANVAS_HEIGHT-height, fill="brown"))
            
    if game_running:
        # move the plane however much it moves during one frame
        plane_x = plane_x - 4 * speed
        if plane_x < -plane_width:
            plane_x += CANVAS_WIDTH
            plane_y = plane_y + 40
            # check we don't go off the bottom of the screen
            if plane_y > CANVAS_HEIGHT:
                plane_y = CANVAS_HEIGHT
            # we get 10 points each row the plane moves down
            score = score + 10

        # we'll check if the plane nose hits a building, or if the
        # base of the fuselage hits.  Won't worry if the wing hits though.
        plane_nose_pos = [plane_x, plane_y + 28]
        plane_body_pos = [plane_x + 12, plane_y + 32]
        for building_num in range(0, 1200//SPACING):
            if ((plane_nose_pos[0] >= building_xpos[building_num]
                 and plane_nose_pos[0] <= building_xpos[building_num] + building_width
                 and plane_nose_pos[1] >= CANVAS_HEIGHT - building_heights[building_num])
                or (plane_body_pos[0] >= building_xpos[building_num]
                 and plane_body_pos[0] <= building_xpos[building_num] + building_width
                 and plane_body_pos[1] >= CANVAS_HEIGHT - building_heights[building_num])):
                # game over
                game_running = False
                won = False
                msg_text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, anchor="c")
                canvas.itemconfig(msg_text, text="GAME OVER!", font=bigfont)

        #have we landed yet?
        if plane_body_pos[1] == CANVAS_HEIGHT and plane_body_pos[0] < 20:
            game_running = False
            won = True
            score = score + 1000
            canvas.itemconfig(score_text, text="Level: " + str(level) + "  Score: " + str(score), font=scorefont)
            msg_text = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, anchor="c")
            canvas.itemconfig(msg_text, text="SUCCESS!", font=bigfont)
            msg_text2 = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2 + 100, anchor="c")
            canvas.itemconfig(msg_text2, text="Press n for next level.", font=scorefont)

        if bomb_falling:
            #move the bomb
            bomb_y = bomb_y + 8 * speed
            #check if the bomb has hit a building
            for building_num in range(0, 1200//SPACING):
                if (bomb_x >= building_xpos[building_num]
                    and bomb_x <= building_xpos[building_num] + building_width
                    and bomb_y >= CANVAS_HEIGHT - building_heights[building_num]):
                    #explode
                    bomb_falling = False
                    #shrink the building
                    building_heights[building_num] = building_heights[building_num] - 50
                    canvas.delete(building_rects[building_num])
                    x = building_xpos[building_num]
                    building_rects[building_num] = canvas.create_rectangle(x, CANVAS_HEIGHT, x + building_width,
                                                                           CANVAS_HEIGHT-building_heights[building_num], fill="brown")
        canvas.delete(plane_body)
        canvas.delete(plane_wing1)
        canvas.delete(plane_wing2)
        canvas.delete(plane_tail)

        #update all the coordinates and redraw the plane
        current_body_points = []
        is_x = True;
        for val in plane_body_points:
            if is_x:
                current_body_points.append(val + plane_x)
            else:
                current_body_points.append(val + plane_y)
            is_x = not is_x
        plane_body = canvas.create_polygon(*current_body_points, fill="red")

        current_wing1_points = []
        is_x = True;
        for val in plane_wing1_points:
            if is_x:
                current_wing1_points.append(val + plane_x)
            else:
                current_wing1_points.append(val + plane_y)
            is_x = not is_x
        plane_wing1 = canvas.create_polygon(*current_wing1_points, fill="grey")

        current_wing2_points = []
        is_x = True;
        for val in plane_wing2_points:
            if is_x:
                current_wing2_points.append(val + plane_x)
            else:
                current_wing2_points.append(val + plane_y)
            is_x = not is_x
        plane_wing2 = canvas.create_polygon(*current_wing2_points, fill="grey")

        current_tail_points = []
        is_x = True;
        for val in plane_tail_points:
            if is_x:
                current_tail_points.append(val + plane_x)
            else:
                current_tail_points.append(val + plane_y)
            is_x = not is_x
        plane_tail = canvas.create_polygon(*current_tail_points, fill="grey")

        if bomb_drawn:
            canvas.delete(bomb_polygon)
        if bomb_falling:
            #calculate the new coordinates
            current_bomb_points = []
            is_x = True;
            for val in bomb_points:
                if is_x:
                    current_bomb_points.append(val + bomb_x)
                else:
                    current_bomb_points.append(val + bomb_y)
                is_x = not is_x
            bomb_polygon = canvas.create_polygon(*current_bomb_points, fill="black")
            bomb_drawn = True
        canvas.itemconfig(score_text, text="Level: " + str(level) + "  Score: " + str(score), font=scorefont)
    root.update()
    framecount = framecount + 1
    # only check every ten frames
    if framecount == 10:
        now = time()
        elapsed = now - lastframe
        # speed will be 1.0 if we're achieving 60 fps
        if speed == 0.0:
            #initial speed value
            # At 60fps, 10 frames take 1/6 of a second.
            speed = 6 * elapsed
        else:
            # use an EWMA to damp speed changes and avoid excessive jitter
            speed = speed * 0.9 + 0.1 * 6 * elapsed
        lastframe = now
        framecount = 0
root.destroy()
