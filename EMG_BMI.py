import pyglet
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import threading
import sys
import os
import math
import subprocess
import statistics
import time
import asyncio
from mock_keys import jump, squat, right, left, clear, down
#Un-comment this if using OS-X.
#os.system('defaults write org.python.python ApplePersistenceIgnoreState NO')

WindowSize = 5000
SampleRate = 1000.0
VoltsPerBit = 2.5/256

#Define global variables
Fs = 1000
FlexWindowSize = 0.25
data = []
displayData = [-2 for i in range(WindowSize)]
flexing = False
time = 0
command = 0
# This reads from a socket.
def data_listener():
  global data
  UDP_PORT = 9000
  sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
  sock.bind((UDP_IP, UDP_PORT))
  while True:
    newdata, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data.extend(list(newdata))

#Handle command line arguments to get IP address
if (len(sys.argv) == 2):
    try:
        UDP_IP = sys.argv[1]
        socket.inet_aton(UDP_IP)
    except:
        sys.exit('Invalid IP address, Try again')
else:
    sys.exit('EMG_Acquire <Target IP Address>')

#Connect the UDP_Port
UDP_PORT = 9000
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

print('Connected to ', str(UDP_IP))
print("Listening for incoming messages...")
print('Close Window to exit')

#Start a new thread to listen for data over UDP
thread = threading.Thread(target=data_listener)
thread.daemon = True
thread.start()

# This is an example for the mocked keyboard events
# Uncomment this example to see how the mocked keyboard
# events affect the mario game!
'''
def example():
  while True:
    time.sleep(3)
    right()

thread2 = threading.Thread(target=example)
thread2.daemon = True
thread2.start()
'''
#Load and place image resources
pyglet.resource.path = ['./resources']
pyglet.resource.reindex()
ForeArm_image = pyglet.resource.image("forearm.png")
Bicep_image = pyglet.resource.image("Bicep.png")
ForeArm_image.anchor_x = 7
ForeArm_image.anchor_y = ForeArm_image.height-150
Bicep_image.anchor_x = Bicep_image.width/2
Bicep_image.anchor_y = Bicep_image.height/2

#Define the moving ForeArm class
class ForeArm(pyglet.sprite.Sprite):
  def __init__(self, *args, **kwargs):
    super(ForeArm,self).__init__(img=ForeArm_image,*args, **kwargs)	
    self.rotate_speed = 100.0
    self.rotation_upper_limit = -10
    self.rotation_lower_limit = -100
    self.rotation = self.rotation_upper_limit
    self.key_handler = pyglet.window.key.KeyStateHandler()

  def update(self, dt):
    if flexing:
      if not ((self.rotation-self.rotate_speed*dt) <=  self.rotation_lower_limit):
        self.rotation -= self.rotate_speed*dt
      else:
        self.rotation = self.rotation_lower_limit
    else:
      if not((self.rotation+self.rotate_speed*dt) >= self.rotation_upper_limit):
        self.rotation += self.rotate_speed*dt
      else:
        self.rotation = self.rotation_upper_limit


#Setup the main window
main_window = pyglet.window.Window(1000,600)
main_batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)
bicep = pyglet.sprite.Sprite(img=Bicep_image,x=350,y=150,batch=main_batch,group=background)
forearm = ForeArm(x=510, y=115,batch=main_batch,group=foreground)
pyglet.gl.glClearColor(1, 1, 1, 1)
main_window.push_handlers(forearm)
main_window.push_handlers(forearm.key_handler)


def update(dt):
  global displayData, data, flexing, time, command

  newData = list(data)

  data = []
  newDisplay = list(displayData[len(newData):len(displayData)] + newData)
  displayData = list(newDisplay)

  #Put your flex algorithm code here!
  #If flexing is detected, set the 'flexing' variable to True.
  #Otherwise, set it to False. 
  #############################
  #ALL OF YOUR CODE SHOULD GO BELOW HERE
  flexing = False
  #command = 0 #command 0 = nothing, 1 = right or left press, 2 = jump, 3 = down command, 4 is placeholder 

  scale = 5

  if len(newData) > 2:
   # print(str(statistics.stdev(newData)))
    if (statistics.stdev(newData) > 15):
      time = 0
      if(command != 2):
        clear()
      command = 2 #jump command  
    #elif (statistics.stdev(newData) > 10):
     # command = 4
      #if time > 150: #some threshold to distinguish between walking and trying to press down or go left
       # command = 3
    elif (statistics.stdev(newData) > 4):
      time = 0
      #print('walk')
      if(command != 1):
        clear()
      command = 1	  
      
    else:
      flexing = False
      time = time + dt
      if(time > 2):
       down(dt)
       left(dt*scale*5)
       
      command = 0 #nothing command
      #time = 0 #when nothing is happening reset timer  
   
  if command == 1:
    #xright walk
    right(dt*scale)
  elif command == 2:
    #jump
    jump(dt*scale*7)
  elif command == 4:
    down(dt)#command = command * -1 #change to walk left and down input
  elif command < 0:
    #left walk
    left(dt*scale)

  #print(str(command))
  #ALL OF YOUR CODE SHOULD GO ABOVE HERE
#__/\\\\\\\\\\\\\____/\\\\____________/\\\\__/\\\\\\\\\\\\\\\_______________/\\\\\\\\\\______/\\\\\\\_________/\\\_        
# _\/\\\/////////\\\_\/\\\\\\________/\\\\\\_\/\\\///////////______________/\\\///////\\\___/\\\/////\\\___/\\\\\\\_       
#  _\/\\\_______\/\\\_\/\\\//\\\____/\\\//\\\_\/\\\________________________\///______/\\\___/\\\____\//\\\_\/////\\\_      
#   _\/\\\\\\\\\\\\\\__\/\\\\///\\\/\\\/_\/\\\_\/\\\\\\\\\\\_______________________/\\\//___\/\\\_____\/\\\_____\/\\\_     
#    _\/\\\/////////\\\_\/\\\__\///\\\/___\/\\\_\/\\\///////_______________________\////\\\__\/\\\_____\/\\\_____\/\\\_    
#     _\/\\\_______\/\\\_\/\\\____\///_____\/\\\_\/\\\_________________________________\//\\\_\/\\\_____\/\\\_____\/\\\_   
#      _\/\\\_______\/\\\_\/\\\_____________\/\\\_\/\\\________________________/\\\______/\\\__\//\\\____/\\\______\/\\\_  
#       _\/\\\\\\\\\\\\\/__\/\\\_____________\/\\\_\/\\\\\\\\\\\\\\\___________\///\\\\\\\\\/____\///\\\\\\\/_______\/\\\_ 
#        _\/////////////____\///______________\///__\///////////////______________\/////////________\///////_________\///_ 
  ###################################
  forearm.update(dt)

@main_window.event
def on_draw():
    main_window.clear()
    main_batch.draw()

pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()