import pygame

pygame.init()
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
controller.init()

while True:
    print(controller.get_axis(0))
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                if event.value > 0:
                    #print(event.value)
                    print(controller.get_axis(0))
           # print(event.value)
        #print(pygame.JOYAXISMOTION)
    #controller.init()
    #print(controller.get_axis(0))
