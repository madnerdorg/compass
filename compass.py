import pygame
from pygame.locals import *
import os
import time
import sys
import math

##############
# COMPASS
##############
import RTIMU
import os.path
import time
import math
SETTINGS_FILE = "RTIMULib"
s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)
poll_interval = imu.IMUGetPollInterval()

##############
# GUI
##############
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen_info = pygame.display.Info()
WINDOW_SIZE = (screen_info.current_w, screen_info.current_h)
surface = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
center_screen_x = WINDOW_SIZE[0] * 0.5
center_screen_y = WINDOW_SIZE[1] * 0.5
# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
#pygame.draw.line(surface, BLUE, (160, 0), (160, 200), 10)
compass_image = pygame.image.load("compass.png").convert_alpha()
compass_rect = compass_image.get_rect()
previous_angle = 0
current_angle = 20
#surface.blit(compass_image,(150,50))

pygame.display.flip()
while True:
    
    if imu.IMURead():
        data = imu.getIMUData()
        magX = data["compass"][0]
        magY = data["compass"][1]
        heading = 180 * math.atan2(magY,magX)/math.pi
        if heading < 0:
            heading += 360
        heading = int(heading)
        print(heading)
        current_angle = heading

    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            sys.exit()
    
    if previous_angle != current_angle:
        rotated_compass = pygame.transform.rotate(compass_image,current_angle)
        compass_pos_x = center_screen_x - (compass_rect.center[0] * 0.5)
        compass_pos_y = center_screen_y - (compass_rect.center[1] * 0.5)
        print(compass_rect.center)
        compass_rect = rotated_compass.get_rect(center=(compass_pos_x,compass_pos_y))
        surface.fill(BLACK)
        surface.blit(rotated_compass,compass_rect)
        pygame.display.flip()
        previous_angle = current_angle
        print(current_angle)
    
    clock.tick(100)
    
    
    #pygame.display.flip()
    #pygame.display.update()
