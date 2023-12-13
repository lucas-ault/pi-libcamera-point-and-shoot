import os
import time
from gpiozero import Button
from datetime import datetime
from signal import pause
from multiprocessing import Process, Queue
from subprocess import Popen

shutterButton = Button(20)
PreviewButton = Button(26)
shutdownButton = Button(21)
x = 0
sleepStaus = 0
k = None
startTimer = 0

def sleepFunction():
    command = "xset dpms force off"
    cmd = command
    p = Popen(cmd.split())
    print("screen off")


def run():
    print("preview is initiated")
    try:
        command = "libcamera-hello -t 5000 --info-text Preview_Display"
        cmd = command
        p = Popen(cmd.split())
        x = p.pid
        print("Process ID:", x)
        while True:
            if p.poll() != None:
                print("preview is closed")
                break;
            else:
                print("waiting for it to take picture")
    except:
        print("error")

def WorkerThread():
    print("capture is initiated")
    # command = "kill "+ str(x)
    # cmd = command
    # p = Popen(cmd.split())
    try:
        location = "/media/pi/SD/"
        name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        command = "libcamera-still -t 3000 -o "+name+".jpg --autofocus-mode auto --info-text Image_Capture"
        cmd = command
        r = Popen(cmd.split())
        k = r.pid
        print(r.poll())
        while True:
            if r.poll() != None:
                print("image capture is closed")
                break;
            else:
                print("waiting for it to take picture")
    except:
        print("error")

while True:
    if (shutterButton.is_pressed == True):
        WorkerThread()
        time.sleep(1)

    elif (PreviewButton.is_pressed == True):
        run()
        time.sleep(1)

    elif (shutdownButton.is_pressed == True):
        pressed_time=time.monotonic()
        while (shutdownButton.is_pressed == True): 
            pass
        pressed_time=time.monotonic()-pressed_time
        if pressed_time<5:
            print("shutdownButton is pressed less then 5 sec")
            sleepFunction()
            time.sleep(0.05)
        elif pressed_time>=5: 
            print("shutdownButton is pressed more then 5 sec")       
            command = "sudo shutdown -h now"
            cmd = command
            p = Popen(cmd.split())
            time.sleep(0.05)
