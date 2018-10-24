#!/usr/bin/python

# import probably too much stuff
import RPi.GPIO as GPIO
import os
import sys
import time
import random
import subprocess 

# set variables that match the pins on the PI for the buttons
simpsonsButton = 17
futuramaButton = 27
disenchantmentButton = 22

# set variables for directories with video files
simpsonsDirectory = "/home/pi/Videos/Simpsons/"
futuramaDirectory = "/home/pi/Videos/Futurama/"
disenchantmentDirectory = "/home/pi/Videos/Disenchantment/"

# initiate variables for use in functions
episode = None
omxc = None
previousEpisode = []

# set up the GPIO stuff for the PI buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(simpsonsButton, GPIO.IN)
GPIO.setup(futuramaButton, GPIO.IN)
GPIO.setup(disenchantmentButton, GPIO.IN)

# functions for each show / button

## works-ish but sloppy and old
def playSimpsons():
    episode = random.choice(os.listdir(simpsonsDirectory))
    os.system('killall omxplayer.bin')
    omxc = subprocess.Popen(['omxplayer', '-b', simpsonsDirectory + episode, ' &'])
    time.sleep(.3)

## working function to use as model for other functions
def playFuturama():
    global episode
    global previousEpisode
    global omxc

    if episode != None:
        previousEpisode.append(episode)

    episode = random.choice(os.listdir(futuramaDirectory))

    while episode in previousEpisode:
        episode = random.choice(os.listdir(futuramaDirectory))

    if omxc != None:
        subprocess.Popen(['killall', 'omxplayer.bin'])

    omxc = subprocess.Popen(['omxplayer', '-b', futuramaDirectory + episode])
    time.sleep(.3)

## works-ish but sloppy and old
def playDisenchantment():
    episode = random.choice(os.listdir(disenchantmentDirectory))
    os.system('killall omxplayer.bin')
    omxc = subprocess.Popen(['omxplayer', '-b', disenchantmentDirectory + episode, ' &'])
    time.sleep(.3)

# main code to wait for button presses.  
try: 
    while True:
        if GPIO.input(simpsonsButton) == 1:
            playSimpsons()
    
        if GPIO.input(futuramaButton) == 1:
            playFuturama()
    
        if GPIO.input(disenchantmentButton) == 1:
            playDisenchantment()

# reset GPIO on ctrl-c
except KeyboardInterrupt:
    GPIO.cleanup()

