## Copyright 2023 by ayouknowwho

## This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, 
## either version 3 of the License, or (at your option) any later version.
## This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
## PARTICULAR PURPOSE. See the GNU General Public License for more details.
## You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

## Imports
import subprocess
import time
import random
import gi
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk
import pynput
from multiprocessing import Manager,Process
manager = Manager()

## Global Vars
# Create the action key matrix: keys in row 0, duration in row 1, timesince in row 3
username = "PUTUSERNAMEHERE"
keymatrix = [1,2,3,4,5,"q","w","e","r","t"],[4.8,6.2,6.1,6.1,4.6,1,1,1,99,1],[0,0,0,0,0,0,0,0,0,0]

# Multiprocessing Queues
queue1 = manager.Queue()
queue2 = manager.Queue()
queue3 = manager.Queue()

## Definitions
def PixelAt(x, y):
    w = Gdk.get_default_root_window()
    pb = Gdk.pixbuf_get_from_window(w, x, y, 1, 1)
    return pb.get_pixels()

# Taking an ingame action by pressing a button and resetting the timer if it recieves a job in queue2
def actionloop():
    global keymatrix
    global queue2
    while (1 == 1):
        if (not queue2.empty()):
            queueget = str(queue2.get())
            if (queueget == "done"):
                break
            time.sleep(random.randrange(1,10,1)*0.001)
            subprocess.run(["xdotool","key","--delay","1",str(queueget)])
        time.sleep(0.01)

# Defines keypress processes for keyboard listener. main ends on key release if loop is ended.
def on_press(key):
    key1 = 0

def on_release(key):
    global queue1
    global queue2
    global queue3

    #if super is pressed toggle the flask drinking state
    if (str(key) == "Key.cmd"):
        queue1.put("toggle")

    #if esc is pressed pass the poison pill, ending the looping subprocess
    if (str(key) == "Key.esc"):
        queue1.put("done")
        queue2.put("done")
        return False

    #to get the poison pill from autologout
    if (not queue3.empty()):
        queueget = str(queue3.get())
        if (queueget == "done"):
            return False

    if (str(key) == "Key.f2"):
        subprocess.run(["xdotool","keydown","--delay","1","Control_L"])
        subprocess.run(["xdotool","key","--delay","1","Return"])
        subprocess.run(["xdotool","keyup","--delay","1","Control_L"])
        subprocess.run(["xdotool","type","--delay","1","1 min plz"])
        subprocess.run(["xdotool","key","--delay","1","Return"])

    if (str(key) == "Key.f3"):
        subprocess.run(["xdotool","key","--delay","1","Return"])
        time.sleep(0.1)
        subprocess.run(["xdotool","type","--delay","1","/kick "])
        subprocess.run(["xdotool","type","--delay","1",username])
        subprocess.run(["xdotool","key","--delay","1","Return"])

    if (str(key) == "Key.f4"):
        subprocess.run(["xdotool","key","--delay","1","Return"])
        time.sleep(0.1)
        subprocess.run(["xdotool","type","--delay","1","/hideout"])
        subprocess.run(["xdotool","key","--delay","1","Return"])

def loop():
    global queue1
    global queue2
    global queue3
    togglestate = False
    firstrun = True
    
    #create desired pixelcolours
    str1 = "(133, 237, 250)"
    str2 = "(112, 73, 43)"

    while (1==1):
        queueget = None
        timesaved=time.time()

        #collect the pixel colours
        str3=str(tuple(PixelAt(207,1030)))
        str4=str(tuple(PixelAt(16,981)))

        #if the pixels do not match the desired colours quit and break the while loop
        if ((str1 != str3) and (str2 == str4)):
            subprocess.run(["xdotool","key","--delay","1","Return"])
            subprocess.run(["xdotool","type","--delay","1","/exit"])
            subprocess.run(["xdotool","key","--delay","1","Return"])
            queue1.put("done")
            queue2.put("done")
            queue3.put("done")
            break

        # If the poison pill is recieved quit and break the while loop
        if (not queue1.empty()):
            queueget = str(queue1.get())
            if (queueget == "done"):
                break

            # Toggle the toggle
            if (queueget == "toggle"):
                togglestate = not togglestate

        #if the togglestate is 1 we start doing actions
        if (togglestate == True):
            #if the loop is new, act. if the loop runs over the action duration time, act and reset timer
            for x in range(1,11):
                if (firstrun == True):
                    queue2.put(str(keymatrix[0][x-1]))
                if (keymatrix[2][x-1] > keymatrix[1][x-1]):
                    queue2.put(str(keymatrix[0][x-1]))
                    keymatrix[2][x-1] = 0
            firstrun = False
        time.sleep(0.01)
        #update the timers
        for x in range(1,11):
            keymatrix[2][x-1] = keymatrix[2][x-1]+(time.time()-timesaved)

##MAIN - KEYBOARD LISTENER
def main():

    loop1 = Process(target=loop,args=())
    loop1.start()
    loop2 = Process(target=actionloop,args=())
    loop2.start()

    # Collect events until released
    with pynput.keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

##AUTO MAIN
if (__name__ == "__main__"):
 main()
