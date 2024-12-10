import pygame
import time
import sys
import pygame_gui
import random
import math

from pygame_gui.elements import UIButton
from pygame_gui.elements import UILabel
from pygame_gui.elements import UITextBox
from pygame_gui.windows import UIColourPickerDialog

pygame.init()

#main screen
WIDTH, HEIGHT = 700, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
surf = pygame.Surface((WIDTH, HEIGHT))
surf.fill(pygame.Color(255, 255, 255))
pygame.display.set_caption("Colors 2048")
BG = pygame.transform.scale(pygame.image.load("2048.png"), (WIDTH, HEIGHT))
RAINBOWBG = pygame.transform.scale(pygame.image.load("rainbow.jpg"), (WIDTH, HEIGHT))
winscreen = pygame.transform.scale(pygame.image.load("win.png"), (WIDTH, HEIGHT))

#current "color" theme is white, mode is rainbow
current_color = pygame.Color(255, 255, 255)
current_mode = "Rainbow"

#color picker
ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')
color_button = UIButton(relative_rect=pygame.Rect(90, 200, 120, 30),
                        text = 'Pick Color',
                        manager = ui_manager)
reset_button = UIButton(relative_rect=pygame.Rect(90, 231, 120, 30),
                        text = 'Reset Color',
                        manager = ui_manager)
current_color = pygame.Color(255, 255, 255)
current_mode = "Rainbow"
WIN.fill(current_color)

#other controls
help_button = UIButton(relative_rect=pygame.Rect(525, 850, 150, 30),
                       text = "Help/Instructions",
                       manager = ui_manager)
show_num_button = UIButton(relative_rect=pygame.Rect(350, 850, 150, 30),
                       text = "Show/Hide Numbers",
                       manager = ui_manager)
help_box = UITextBox(
                html_text="Welcome to 2048 (Colors Edition)! \n\n" +
                "The objective of this game is simple: combine like-numbered tiles until "+
                "you reach the final number, 2048.\n\n" +
                "Use the arrow keys or WASD to control the tiles: pressing the left key will shift " +
                "all the numbers as far left as they can (imagine 'tipping' the image to the left), " +
                "pressing the up key will shift all the numbers to the top, and so on and so forth. \n\n" +
                "When two colors/numbers of the same value are pushed together, they will combine, " +
                "double in value, and change colors.\n\n"+
                "Click Show/Hide Numbers to toggle whether the values for each square are displayed or not."+
                "\n\nIf you get stuck (or simply want to reset or replay), press R to restart the game, and Q to quit." +
                "\n\n Good Luck!",
                relative_rect=pygame.Rect(80, 285, 540, 540),
                manager=ui_manager)
help_x = UIButton(relative_rect = pygame.Rect(615, 285, 20, 20),
                  text = "X",
                  manager = ui_manager)
help_box.hide()
help_x.hide()
help_x.disable()
clock = pygame.time.Clock()
gameover = False

#start
WIN.blit(RAINBOWBG, (0, 0))
WIN.blit(BG, (0, 0))

val = [[0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0],
       [0, 0, 0, 0]]
colors = ["LightCoral", "OrangeRed", "Orange", "Yellow", "LawnGreen", "DarkGreen",
          "DarkCyan", "Blue", "DarkSlateBlue", "Indigo", "Purple"]
xpos = [82, 214, 345, 480]
ypos = [285, 420, 555, 690]
filled = 0
score = 0
maxscore = 0
maxcolor = "LightCoral"
maxnum = 2

def spawn():
    global filled
    global val
    global gameover
    filled = filled + 1
    #if (filled == 16):
        #gameover = True
    a = random.randint(0, 3)
    b = random.randint(0, 3)
    while (val[a][b] != 0 and filled != 16):
        a = random.randint(0, 3)
        b = random.randint(0, 3)
    val[a][b] = pow(2, random.randint(0, 2)%2 +1)

hold = False
shownum = 0
oppcol = "white"

a = random.randint(0, 3)
b = random.randint(0, 3)
val[a][b] = pow(2, random.randint(0, 2)%2 +1)
spawn()

def fadeout(i, j, newi, newj):
    shift(a)

#game
won = False
won1 = False
while True:
    time_delta = clock.tick(60)/1000

    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == color_button:
            color_picked = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                ui_manager,
                                                window_title = "Change Color...",
                                                initial_colour = current_color)
            color_button.disable()
            reset_button.disable()
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == reset_button:
            current_mode = "Rainbow"
            colors = ["#ff0000", "#ff5300", "#ffa500", "#ffd200", "#ffff00",
                      "#80c000", "#008000", "#004080", "#0000ff", "#2600c1", "#4b0082"]
            colors = ["LightCoral", "OrangeRed", "Orange", "Yellow", "LawnGreen", "DarkGreen",
                      "DarkCyan", "Blue", "DarkSlateBlue", "Indigo", "Purple"]
            oppcol = "white"
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == help_button:
            help_box.show()
            help_x.show()
            help_x.enable()
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == help_x:
            help_box.hide()
            help_x.disable()
            help_x.hide()
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == show_num_button:
            shownum += 1
            shownum %= 2
        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            current_mode = "Manual"
            current_color = event.colour
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            color_button.enable()
            reset_button.enable()
            color_picked = None
        #if playing the game
        if gameover == False:
            if event.type == pygame.KEYDOWN:
                change = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    won = False
                    won1 = False
                    score = 0
                    color_button.show()
                    color_button.enable()
                    reset_button.show()
                    reset_button.enable()
                    help_button.show()
                    help_button.enable()
                    show_num_button.show()
                    show_num_button.enable()
                    val = [[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]]
                    a = random.randint(0, 3)
                    b = random.randint(0, 3)
                    val[a][b] = pow(2, random.randint(0, 2)%2 +1)
                    spawn()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    #check once
                    for j in range(4):
                        nums = []
                        count = 0
                        for i in range(4):
                            if val[i][j] != 0:
                                nums.append(val[i][j])
                                count += 1
                        if (count != 4):
                            change = True
                        for i in range(4):
                            if (i < len(nums)):
                                val[i][j] = nums[i]
                            else:
                                val[i][j] = 0
                    #merge
                    
                    for j in range(4):
                        for i in range(0, 3):
                            if val[i][j] == val[i+1][j] and val[i+1][j] != 0:
                                change = True
                                val[i][j] *= 2
                                score += val[i][j]
                                val[i+1][j] = 0
                                i = 0
                    #check again
                    for j in range(4):
                        nums = []
                        count = 0
                        for i in range(4):
                            if val[i][j] != 0:
                                nums.append(val[i][j])
                                count += 1
                        if (count != 4):
                            change = True
                        for i in range(4):
                            if (i < len(nums)):
                                val[i][j] = nums[i]
                            else:
                                val[i][j] = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    #check once
                    for j in range(4):
                        nums = []
                        count = 0
                        for i in range(4):
                            if val[i][j] != 0:
                                nums.append(val[i][j])
                                count += 1
                        if (count != 4):
                            change = True
                        for i in range(4-count):
                            val[i][j] = 0
                        for i in range(count):
                            val[i+(4-count)][j] = nums[i]
                    #merge
                    
                    for j in range(4):
                        for i in range(3, 0, -1):
                            if val[i][j] == val[i-1][j] and val[i-1][j] != 0:
                                change = True
                                val[i][j] *= 2
                                score += val[i][j]
                                val[i-1][j] = 0
                                i = 0
                    #check again
                    for j in range(4):
                        nums = []
                        count = 0
                        for i in range(4):
                            if val[i][j] != 0:
                                nums.append(val[i][j])
                                count += 1
                        if (count != 4):
                            change = True
                        for i in range(4-count):
                            val[i][j] = 0
                        for i in range(count):
                            val[i+(4-count)][j] = nums[i]
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    for i in range(4):
                        #check once
                        nums = []
                        count = 0
                        for j in range(4):
                            if val[i][j] != 0:
                                nums.append(val[i][j])
                                count = count + 1
                        if (count != 4):
                            change = True
                        val[i] = nums
                        val[i].extend([0]*(4-count))
                    #merge
                    for i in range(4):
                        for j in range(3):
                            if val[i][j] == val[i][j+1] and val[i][j] != 0:
                                change = True
                                val[i][j] *= 2
                                score += val[i][j]
                                val[i][j+1] = 0
                                j = 0
                        #check again
                    for i in range(4):
                        nums = []
                        count = 0
                        for j in range(4):
                            if val[i][j] != 0:
                                nums.append(val[i][j])
                                count += 1
                        if (count != 4):
                            change = True
                        val[i] = nums
                        val[i].extend([0]*(4-count))
                if event.key == pygame.K_RIGHT or event.key == pygame.K_s:
                    for i in range(4):
                        #check once
                        nums = []
                        count = 0
                        for j in range(4):
                            if val[i][j] != 0:
                                nums.append(val[i][j])
                                count+=1
                        if (count != 4):
                            change = True
                        val[i] = [0]*(4-count)
                        val[i].extend(nums)
                        #merge
                    for i in range(4):
                        for j in range(3, 0, -1):
                            if val[i][j] == val[i][j-1] and val[i][j] != 0:
                                change = True
                                val[i][j] *= 2
                                score += val[i][j]
                                val[i][j-1] = 0
                                j = 0
                        #check again
                    for i in range(4):
                        nums = []
                        count = 0
                        for j in range(4):
                            if val[i][j] != 0:
                                nums.append(val[i][j])
                                count+=1
                        if (count != 4):
                            change = True
                        val[i] = [0]*(4-count)
                        val[i].extend(nums)
                if (change == True):
                    spawn()
                    
                
        if event.type == pygame.KEYUP:
            hold = False

        ui_manager.process_events(event)

    WIN.blit(surf, (0, 0))
    #prototype code
    color = "white"
    oppcol = "white"
    
    myf = pygame.font.SysFont("comicsans", 30)
    maxnum = 2
    for i in range(4):
        for j in range(4):
            if (val[i][j] == 2048):
                won = True
            if (val[i][j] != 0):
                color = colors[int(math.log(val[i][j], 2)-1)]
            else:
                color = "white"
            if (val[i][j]>maxnum):
                maxnum = val[i][j]
            if (score > maxscore):
                maxscore = score
            pygame.draw.rect(WIN, color, pygame.Rect(xpos[j], ypos[i], 135, 135))
            if shownum == 1 and val[i][j] != 0:
                label = myf.render(str(val[i][j]), 1, oppcol)
                WIN.blit(label, (xpos[j]+55, ypos[i]+45))
                
    

    if (current_mode == "Rainbow"):
        surf.blit(RAINBOWBG, (0, 0))
    else:
        surf.fill(current_color)
        
    ui_manager.update(time_delta)

    WIN.blit(BG, (0, 0))
    myfont = pygame.font.SysFont("comicsans", 16)
    maxcolor = colors[int(math.log(maxnum, 2)-1)]
    label = myfont.render(str(score), 1, oppcol)
    WIN.blit(label, (310, 150))
    label = myfont.render(str(maxscore), 1, oppcol)
    WIN.blit(label, (525, 150))
    label = myfont.render(maxcolor, 1, oppcol)
    WIN.blit(label, (280, 220))
    label = myfont.render(str(maxnum), 1, oppcol)
    WIN.blit(label, (527, 220))
    

    if(won1):
        time.sleep(1)
        WIN.blit(winscreen, (0, 0))
    
    if(won):
        won1=True
        color_button.hide()
        color_button.disable()
        reset_button.hide()
        reset_button.disable()
        help_button.hide()
        help_button.disable()
        show_num_button.hide()
        show_num_button.disable()
    
    ui_manager.draw_ui(WIN)

    pygame.display.update()
