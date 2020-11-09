import pynput
import time 
from pynput.keyboard import Key, Controller
keyboard = Controller()
import asyncio
from queue import Queue
import threading

# Keyboard controls for the mario game
'''
This function is written in a functional style.
press_duration is a function that returns functions!
This technique is known as currying with higher-order functions
'''
q = Queue()

def create_action(key):
  def action(duration):
    q.put({'time': duration, 'key': key})
  return action

def consumer():
  while True:
    data = q.get()
    keyboard.press(data['key'])
    time.sleep(data['time'])
    keyboard.release(data['key'])
    time.sleep(0.01)	

keypresser = threading.Thread(target=consumer)
keypresser.daemon = True
keypresser.start()
def clear():
  with q.mutex:
    q.queue.clear()
keys = ['x', Key.down, Key.right, Key.left, Key.down]
# These are the faked-keyboard events
# alxl of these take durations 
jump, squat, right, left, down = map(create_action, keys)