
import pygame
import random
from pygame import mixer

victory = False

# Define a clock here to stop running a program too fast
my_clock = pygame.time.Clock()
FPS = 60

# open window here
cube = 75
half_cube = cube/2
width, height = cube*19 , cube*11
pygame.init()
my_win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Daniels Pack man game")


#Here we create a class for the player character and give basic attributes
class Pac_Man:
    def __init__(self, x, y):
        self.size = 72
        self.dir = [5, 0]
        self.right ,self.left, self.up, self.down= [] , [], [], []
        self.idx = 0
        self.is_ghost = False

        # this for loop load in 10 pictures to right-, left-, up- and down-list of pictures
        for pic in range (10):
            self.right.append(pygame.image.load("pacman/{}.png".format(pic)))
            self.left.append(pygame.transform.flip(self.right[pic], True, False))
            self.up.append(pygame.transform.rotate(self.right[pic],90))
            self.down.append(pygame.transform.rotate(self.right[pic], -90))
        self.pictures = self.right

        #this create a rectangle what is extramly powerfull object for check collusions
        self.rect = self.pictures[0].get_rect()
        self.rect.x = x
        self.rect.y = y

    #this method draw the pack man into screen and pic a next picture from the list
    def draw(self):
        my_win.blit(self.pictures[self.idx],self.rect)
        self.idx = self.idx + 1
        if self.idx > 9 : self.idx = 0

    def move(self):
        self.rect.x = self.rect.x+ self.dir[0]
        self.rect.y = self.rect.y+ self.dir[1]

        if self.rect.x > width : self.rect.x = 0
        if self.rect.y > height: self.rect.y = 0
        if self.rect.x < 0: self.rect.x = width
        if self.rect.y <0: self.rect.y = height

#****************************************************************#
#Here we create a class for enemies and give them basic attributes
class ghost:
    def __init__(self, x, y):
        self.size = 72
        self.dir = [5, 0]
        self.right ,self.left, self.up, self.down= [] , [], [], []
        self.is_ghost = True
        self.img_slow = 0
        self.idx = 0
        self.speed = 2

        #this for loop load in 10 pictures to right-, left-, up- and down-list of pictures
        for pic in range (10):
            self.right.append(pygame.image.load("ghost/{}.png".format(pic)))
            self.left.append(pygame.transform.flip(self.right[pic], True, False))
            self.up.append(pygame.transform.rotate(self.right[pic],90))
            self.down.append(pygame.transform.rotate(self.right[pic], -90))
        self.pictures = self.right


        #this create a rectangle for collusions
        self.rect = self.pictures[0].get_rect()
        self.rect.x = x
        self.rect.y = y

    #this method draw the ghost into screen and pic a next picture from the list
    def draw(self):
        my_win.blit(self.pictures[self.idx], self.rect)
        self.img_slow += 1
        if self.img_slow > 6:
            self.img_slow = 0
            self.idx = self.idx + 1
            if self.idx > 9: self.idx = 0

    # this method move the ghost: add into coordinates his directions
    def move(self):
        self.rect.x = self.rect.x + self.dir[0]
        self.rect.y = self.rect.y + self.dir[1]

        if self.rect.x > width: self.rect.x = 0
        if self.rect.y > height: self.rect.y = 0
        if self.rect.x < 0: self.rect.x = width
        if self.rect.y < 0: self.rect.y = height

    #this method will center the ghost and turn into random direction
    def turn(self):
        #ceneter verticaty
        position_x = self.rect.x % cube
        if position_x > half_cube:
            self.rect.x += cube - position_x
        else:
            self.rect.x -= position_x

        #center horisontaly
        position_y = self.rect.y % cube
        if position_y > half_cube:
            self.rect.y += cube - position_y
        else:
            self.rect.y -= position_y

        # give random directions
        directions = random.randint(0,4)
        print(directions)
        if directions == 0:
            self.dir = [-1*self.speed,0]
            self.pictures = self.left
        elif directions == 1:
            self.dir = [self.speed,0]
            self.pictures = self.right
        elif directions == 2:
            self.dir = [0,-1*self.speed]
            self.pictures = self.up
        elif directions == 3:
            self.dir = [0,self.speed]
            self.pictures = self.down

#**************************************************************************#
#Here we create a sub class of ghost class for creating new type of enemies#
class ghost_boss(ghost):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.speed = 5
        self.right, self.left, self.up, self.down = [], [], [], []

        #this for loop load in 10 pictures to right-, left-, up- and down-list of pictures
        for pic in range (10):
            self.right.append(pygame.image.load("boss_ghost/{}.png".format(pic)))
            self.left.append(pygame.transform.flip(self.right[pic], True, False))
            self.up.append(pygame.transform.rotate(self.right[pic],90))
            self.down.append(pygame.transform.rotate(self.right[pic], -90))
        self.pictures = self.right

#*************************************************************#
#Here we create a wall rectangle objs and draw them into screen
class wall:
    def __init__(self, start_x, start_y , wall_width,  wall_height):
        self.rect = pygame.Rect(start_x, start_y , wall_width,  wall_height)

    def draw(self):
        pygame.draw.rect(my_win,(20,20,200),self.rect)
        pygame.draw.rect(my_win,(40,40,220),(self.rect.x+2,self.rect.y+2,34,10))
        pygame.draw.rect(my_win,(60,60,220),(self.rect.x+38,self.rect.y+2,34,10))
        pygame.draw.rect(my_win,(40,40,220),(self.rect.x+20,self.rect.y+20,34,10))
        pygame.draw.rect(my_win,(50,50,220),(self.rect.x+38,self.rect.y+40,34,10))

#*************************************************************#
#Here we create a pick ups class
class pick_ups:
    # this create a basic attributes and rectangle for collusions
    def __init__(self,x,y):
        self.pic = pygame.image.load("ball/0.png")
        self.pic = pygame.transform.scale(self.pic,(20,20))

        self.rect = self.pic.get_rect()
        self.rect.x = x+27
        self.rect.y = y+27

    # draw into screen
    def draw(self):
        my_win.blit(self.pic, self.rect)

# delete screen with brick texture
def delete_screen():
    my_win.fill((0,0,0))
    for XX in range (cube,19*cube,cube):
        for YY in range (cube,12*cube,cube):
            pygame.draw.rect(my_win, (5, 5, 30), (XX + 2, YY + 2, 34, 10))
            pygame.draw.rect(my_win, (10, 6, 45), (XX + 38, YY + 2, 34, 10))
            pygame.draw.rect(my_win, (5, 5, 30), (XX + 20, YY + 20, 34, 10))
            pygame.draw.rect(my_win, (5, 5, 20), (XX + 38, YY + 40, 34, 10))


#*************************************************************#
#this is a function for start level 1
def start_level1():
    # do a list for moving objs
    all_objs = []
    all_objs.append(Pac_Man(cube,cube))
    all_objs.append(ghost(cube*12,cube))
    all_objs.append(ghost(cube*2, cube*8))
    all_objs.append(ghost_boss(cube*12, cube*8))

    # read txt file to order to create a map = pickups and walls
    text_file = open("map1.txt","r")
    all_map = text_file.readlines()
    map_x, map_y = 0, 0
    all_walls, all_pick_ups = [] , []

    for line in all_map:
        print(line)
        for char in line:
            print(char)
            if char == "#":
                all_walls.append(wall(map_x, map_y, cube, cube))
            elif char == ".":
                all_pick_ups.append(pick_ups(map_x,map_y))

            map_x += cube
        map_y += cube
        map_x = 0

    #Call in sound files and play background music
    pygame.mixer.music.load("sounds/main_theme.wav")
    pygame.mixer.music.play(-1)
    pick_up_sound = mixer.Sound("sounds/pickup.wav")

    #create a game loop
    Game_is_on = True
    while Game_is_on:

        # check for user input
        for event in pygame.event.get():
            pass
        user_input = pygame.key.get_pressed()

        # change pack man direction for arrow keys
        if user_input[pygame.K_LEFT]:
            all_objs[0].dir = [-5, 0]
            all_objs[0].pictures = all_objs[0].left
        elif user_input[pygame.K_RIGHT]:
            all_objs[0].dir = [5, 0]
            all_objs[0].pictures = all_objs[0].right
        elif user_input[pygame.K_UP]:
            all_objs[0].dir = [0, -5]
            all_objs[0].pictures = all_objs[0].up
        elif user_input[pygame.K_DOWN]:
            all_objs[0].dir = [0, 5]
            all_objs[0].pictures = all_objs[0].down

        # Put packman in a center when its turning
        if user_input[pygame.K_UP] or user_input[pygame.K_DOWN]:
            position = all_objs[0].rect.x % cube
            if position > half_cube:
                all_objs[0].rect.x += cube - position
            else:
                all_objs[0].rect.x -= position
        if user_input[pygame.K_LEFT] or user_input[pygame.K_RIGHT]:
            position = all_objs[0].rect.y % cube
            if position > half_cube:
                all_objs[0].rect.y += cube - position
            else:
                all_objs[0].rect.y -= position
        if user_input[pygame.K_ESCAPE]:
            Game_is_on = False

        delete_screen()

        for this_pick_up in all_pick_ups:
            this_pick_up.draw()

        # move and draw moving objs
        for obj in all_objs:
            obj.move()
            obj.draw()

            #checks collusion between pack man and ghost
            if obj.rect.colliderect(all_objs[0]) and obj.is_ghost:
                Game_is_on = False

            #checks collusion between pack man and pick up. If yes Pick up removed
            for this_pick_up in all_pick_ups:
                if this_pick_up.rect.colliderect(all_objs[0]):
                    all_pick_ups.remove(this_pick_up)
                    pick_up_sound.play()

        for this_wall in all_walls:
            this_wall.draw()

            #checks collusion between moving obj and wall
            for obj in all_objs:
                if this_wall.rect.colliderect(obj.rect):
                    obj.rect.x -= obj.dir[0]
                    obj.rect.y -= obj.dir[1]
                    no_effect = True

                    if not obj.is_ghost:
                        obj.dir = [0,0]
                    else:
                        obj.turn()

        if all_pick_ups == []:
            global victory
            Game_is_on = False
            victory = True

        pygame.display.update()
        my_clock.tick(FPS)

# This part is responsible if a game is ended, having delay and let player know the game is over
def game_over():
    pygame.mixer.music.load("sounds/game_over.wav")
    pygame.mixer.music.play()
    for wait_more in range (3):
        my_clock.tick(1)
    start_level1()

# This part is responsible if the player is winning, having delay and let player know hi is win the game
def win_the_game():
    pygame.mixer.music.load("sounds/victory.wav")
    pygame.mixer.music.play()
    for wait_more in range (3):
        my_clock.tick(1)

start_level1()

if not victory:
    game_over()
else:
    win_the_game()

