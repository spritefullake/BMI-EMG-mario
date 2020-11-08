import pynput
import time 
from pynput.keyboard import Key, Controller
keyboard = Controller()

# Keyboard controls for the mario game
'''
This function is written in a functional style.
press_duration is a function that returns functions!
This technique is known as currying with higher-order functions
'''
def press_duration(duration=0.5):
  def create_action(key):
    def action():
      keyboard.press(key)
      # have a delay between pressing the key and releasing
      # so the sprite has time to move a distance
      time.sleep(duration)
      keyboard.release(key)
    return action
  return create_action

create_action = press_duration()
keys = [Key.up, Key.down, Key.right, Key.left]
# These are the faked-keyboard events
jump, squat, right, left = map(create_action, keys)