## Copyright 2023 by ayouknowwho

## This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, 
## either version 3 of the License, or (at your option) any later version.
## This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
## PARTICULAR PURPOSE. See the GNU General Public License for more details.
## You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import subprocess
import time
import random
import gi
import pynput
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk
from multiprocessing import Manager,Process

manager = Manager()
username = "PUTUSERNAMEHERE"
key_matrix = [1,2,3,4,5,"q","w","e","r","t"],[4.8,6.2,6.1,6.1,4.6,1,1,1,99,1],[0,0,0,0,0,0,0,0,0,0]  # keys, interval, time_since_press
control_loop_queue = manager.Queue()
key_queue = manager.Queue()
listener_control_queue = manager.Queue()
sleep_time = 0.01


def main():
    control_loop = Process(target=control_loop,args=())
    control_loop.start()
    keypress_loop = Process(target=keypress_loop,args=())
    keypress_loop.start()

    # Collect events until released
    with pynput.keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()


def check_matrix(first_run):
    global key_queue
    # For each of the ten keys in the matrix
    for i in range(10):
        # If this is the first time through the loop, press the key
        if first_run == True:
            key_queue.put(str(keymatrix[0][i]))
        # If the time has run past the interval, press the key and reset the timer
        elif (keymatrix[2][i] > keymatrix[1][i]):
            key_queue.put(str(keymatrix[0][i]))
            key_matrix[2][i] = 0


def poison(control_bool, key_bool, listen_bool):
    global control_loop_queue
    global key_queue
    global listener_control_queue
    if control_bool:
        control_loop_queue.put("poison")
    if key_bool:
        key_queue.put("poison")
    if listen_bool:
        listener_control_queue.put("poison")
        
        
def quit():
    subprocess.run(["xdotool","key","--delay","1","Return"])
    subprocess.run(["xdotool","type","--delay","1","/exit"])
    subprocess.run(["xdotool","key","--delay","1","Return"])
    poison(True, True, True)

            
# Gets pixel at location (x, y)
def pixel_at(x, y):
    w = Gdk.get_default_root_window()
    pb = Gdk.pixbuf_get_from_window(w, x, y, 1, 1)
    return pb.get_pixels()


# Wait for keys in key_queue and press them
def keypress_loop():   
    global key_matrix
    global key_queue
    while True:
        if (!key_queue.empty()):
            queue_get = str(key_queue.get())
            if (queue_get == "poison"):
                break
            time.sleep(random.randrange(1,10,1)*0.001) # Add some randomness so we don't look like a robot
            subprocess.run(["xdotool","key","--delay","1",queue_get])
        time.sleep(sleep_time)

        
# Defines keypress processes for keyboard listener. main ends on key release if loop is ended.
def on_press(key):
    key1 = 0
    
    
# Request user waits while I'm busy
def f2_macro:
    subprocess.run(["xdotool","keydown","--delay","1","Control_L"])
    subprocess.run(["xdotool","key","--delay","1","Return"])
    subprocess.run(["xdotool","keyup","--delay","1","Control_L"])
    subprocess.run(["xdotool","type","--delay","1","1 min plz"])
    subprocess.run(["xdotool","key","--delay","1","Return"])
    

# Log self out
def f3_macro:
    subprocess.run(["xdotool","key","--delay","1","Return"])
    time.sleep(0.1)
    subprocess.run(["xdotool","type","--delay","1","/kick "])
    subprocess.run(["xdotool","type","--delay","1",username])
    subprocess.run(["xdotool","key","--delay","1","Return"])
    
    
# Go to hideout
def f4_macro:
    subprocess.run(["xdotool","key","--delay","1","Return"])
    time.sleep(0.1)
    subprocess.run(["xdotool","type","--delay","1","/hideout"])
    subprocess.run(["xdotool","key","--delay","1","Return"])

    
def on_release(key):
    global control_loop_queue
    global key_queue
    global listener_control_queue
    key_str = str(key)

    # Check for poison pill
    if !listener_control_queue.empty():
        queue_get = str(listener_control_queue.get())
        if queue_get == "poison":
            return False
        
    # If super is pressed toggle the flask drinking state
    if key_str == "Key.cmd":
        control_loop_queue.put("toggle")

    # If esc is pressed the end the script
    elif key_str == "Key.esc":
        quit()
        return False
    
    elif (key_str == "Key.f2"):
        f2_macro()

    elif (key_str == "Key.f3"):
        f3_macro()

    elif (key_str == "Key.f4"):
        f4_macro()

        
def pixels_check():
    match_pixel = (133, 237, 250)
    unmatch_pixel = (112, 73, 43)
    if (match_pixel == tuple(pixel_at(207,1030)) and (unmatch_pixel != tuple(pixel_at(16,981)):
        return True
    else:
        return False
        
        
def control_loop():
    global control_loop_queue
    toggle_state = False
    first_run = True

    while True:
        start_time = time.time()

        # End the script if pixels aren't how we want them
        if !pixels_check():
            quit()
            break

        # End this loop if the poison pill is recieved
        if !control_loop_queue.empty():
            queue_get = str(control_loop_queue.get())
            if (queue_get == "poison"):
                break
            else:   # queue_get == "toggle"
                toggle_state = !toggle_state

        if toggle_state == True:
            check_matrix(first_run)
        if first_run == True:
            first_run = False
        time.sleep(sleep_time)
        elapsed_time = time.time() - start_time
        
        # Update the timers
        for i in range(10):
            keymatrix[2][i] = keymatrix[2][i] + elapsed_time


if (__name__ == "__main__"):
    main()
