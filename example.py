import pygame, sys
from pygame.locals import *

TIMER = 30
SCREEN_X = 200
SCREEN_Y = 200

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
clock = pygame.time.Clock() #tick-tock

ending = button1 = button2 = False

corner1 = (28,18)  #Top Left corner of button 1
corner2 = (56,18)  #Top Left corner of button 2

image_length = 100 #length of the buttons
image_height = 100 #height of the buttons

counter = 0

#Main Loop:
while ending==False:
    counter+=1
    clock.tick(TIMER)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                ending=True # Time to leave
                print("Game Stopped Early by user")
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if (mouse_x >= corner1[0]) and (mouse_x <= corner1[0]+image_length) and (mouse_y >= corner1[1]) and (mouse_y <= corner1[1]+image_height):
                    print ("Button one is selected")
                    button1=True
                    button2=False
                elif (mouse_x >= corner2[0]) and (mouse_x <= corner2[0]+image_length) and (mouse_y >= corner2[1]) and (mouse_y <= corner2[1]+image_height):
                    print ("Button two is selected")
                    button1=False
                    button2=True
                else:
                    print ("That's not a button")
                    button1=False
                    button2=False
    if counter == TIMER:  #prints the statements once a second
        counter=0
        if button1==True:
            print ("Button one is currently selected")
        elif button2==True:
            print ("Button two is currently selected")
        else:
            print ("No buttons currently selected")