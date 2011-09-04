#!/usr/bin/python3
#
# Simple (hopefully) script to do countdown timer stuff. Created to fill the
# void left by gnome's timer applet when switching to a tiling wm.
#
# @author Matthew Todd
# @date Sep 3 2011

# TODO: program options
#   specify duration
#   specify progress bar length
#   enable/disable sound
#   enable/disable notify-send
#   specify task (msg for notify-send)
#   specify refresh rate (sleep duration)?

import time
import sys
import os
import subprocess

def getDuration():
    '''
    Gets the input from the user regarding the timer's duration/end time.
    @return (duration, endtime)
    '''
    done = False
    while not done:
        duration = input("Enter timer duration (in secs): ")        # TODO: handle other time formats
        try:
            duration = int(duration, 10)
            done = True
        except Exception as e:
            print("Invalid duration: %r" % duration)

    startTime = time.time()
    endTime = startTime + duration
    return (duration, endTime)

def get_screen_width():
    '''
    Gets the terminal width in characters.
    '''
    info = subprocess.check_output(['stty', 'size'])
    _, screen_width = info.split()
    return int(screen_width) 


def main():
    duration, endTime = getDuration()

    currentTime = time.time()
    while currentTime < endTime:
        currentTime = time.time()

        screen_width = get_screen_width() - 10                           # TODO: magic numbers (this one is for time remaining)

        timeLeft = endTime - currentTime
        percentageTime = (duration - timeLeft) / duration
        percentageLength = int(screen_width*percentageTime)

        print("[%s%s]  %d \r" % ('='*percentageLength, '-'*(screen_width-percentageLength), timeLeft), end="")
        sys.stdout.flush()
        time.sleep(.1)      # TODO: make sleep time dynamic?
                            # so that the progress bar is smooth (but will want to make the max 1 sec)


    print("\nFINISHED!")

    # TODO: make func?
    subprocess.call(['notify-send', 'FINISHED!'])       # TODO: more informative message (get user msg?)

    # TODO: play sound

    return 0

if __name__ == '__main__':
    sys.exit(main())

