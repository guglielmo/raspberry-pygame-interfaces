import pygame
from pygame.locals import *
import os
from time import sleep
import RPi.GPIO as GPIO
 
#Note #21 changed to #27 for rev2 Pi
button_map = {23:(255,0,0), 22:(0,255,0), 27:(0,0,255), 17:(0,0,0)}
 
#Setup the GPIOs as inputs with Pull Ups since the buttons are connected to GND
GPIO.setmode(GPIO.BCM)
for k in button_map.keys():
    GPIO.setup(k, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
#Colours
WHITE = (255,255,255)
 
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode([320, 240])
lcd.fill((0,0,0))
pygame.display.update()
 
font_big = pygame.font.Font(None, 50)

touch_buttons = {'left':(80,60), 'right':(240,60),}

# touch buttons 
for k,v in touch_buttons.items():
    text_surface = font_big.render('%s'%k, True, WHITE)
    rect = text_surface.get_rect(center=v)
    lcd.blit(text_surface, rect)
 
pygame.display.update()

print pygame.display.Info()

while True:
    # Scan the buttons
    for (k,v) in button_map.items():
        if GPIO.input(k) == False:
            lcd.fill(v)
            text_surface = font_big.render('%d'%k, True, WHITE)
            rect = text_surface.get_rect(center=(160,120))
            lcd.blit(text_surface, rect)
            pygame.display.update()

    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            print "MOUSEBOTTONDOWN: ", pos
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            print "MOUSEBOTTOMUP: ", pos
            #Find which quarter of the screen we're in
            x,y = pos
            if x < 160:
                print "LEFT PRESSED", pos
            else:
                print "RIGHT RELEASED", pos

    sleep(0.1)



