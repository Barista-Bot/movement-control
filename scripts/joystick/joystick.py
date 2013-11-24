#!/usr/bin/env python

import pygame
import math

class Joystick:
    def __init__(self, joystick_id = 0):
        self.joysticks = []
        try:
            pygame.joystick.init()
            pygame.display.init()
            if not pygame.joystick.get_count():
                print "No Joysticks detected. Please connect a joystick."
                quit()
            print "%d joystick(s) detected." % pygame.joystick.get_count()
            
            for i in range(pygame.joystick.get_count()):
                js = pygame.joystick.Joystick(i)
                js.init()
                self.joysticks.append(js)
                print js.get_numaxes()
                print "Joystick %d: " % (i) + self.joysticks[i].get_name()
         
            self.setActiveJoystick(joystick_id);
        except pygame.error:
            print 'No joystick with id ' + str(joystick_id) + ' found'
        return
        
    def setActiveJoystick(self,active_js = 0):
        if len(self.joysticks) < (active_js - 1):
            print 'Error: no such joystick id'
            return
        self.active_js = active_js
        
    def getXVal(self):
        pygame.event.pump()
        return -1.0*float(self.joysticks[self.active_js].get_axis(1))
    
    def getYVal(self):
        pygame.event.pump()
        return -1.0*float(self.joysticks[self.active_js].get_axis(0))
    
    def isInit(self):
        return (self.joysticks[self.active_js]).get_init()
    
