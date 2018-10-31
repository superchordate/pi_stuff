#!/usr/bin/python

import RPi.GPIO as GPIO
import os
import sys
import time
import random
import subprocess

episode = None
omxc = None
previousEpisode = []
    
def playEp( directory ):
    
    global episode, omxc, previousEpisode
    
    if episode != None: previousEpisode.append(episode)
    
    episode = random.choice( os.listdir(directory) )

    while episode in previousEpisode:
        episode = random.choice(os.listdir(directory))
    
    if omxc != None:
        subprocess.Popen( [ 'killall', 'omxplayer.bin' ] )
    else:
        os.system( 'killall omxplayer.bin' )
        
    omxc = subprocess.Popen( [ 'omxplayer', '-b', simpsonsDirectory + episode, ' &' ] )
    
def playSimpson():
    playEp( "/home/pi/Videos/Simpsons/" )
    
def playFuturama():
    playEp( "/home/pi/Videos/Futurama/" )
    
def playDisen():
    playEp( "/home/pi/Videos/Disenchantment/" )
    
def cleanUp():
    GPIO.cleanup()

# button setup and listeners.
# from http://raspberry.io/projects/view/reading-and-writing-from-gpio-ports-from-python/

GPIO.setmode(GPIO.BCM)

def addCallback( buttonNum, callback ):
    
    GPIO.setup( buttonNum, GPIO.IN, pull_up_down = GPIO.PUD_DOWN )
    GPIO.add_event_detect( buttonNum, GPIO.BOTH )
    GPIO.add_event_callback( buttonNum, callback)

addCallback( 17, playSimpson )
addCallback( 27, playFuturama )
addCallback( 22, playSimpson )

# Also add callback for ctrl+c?