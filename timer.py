#!/usr/bin/python3
#
# Simple (hopefully) script to do countdown timer stuff. Created to fill the
# void left by gnome's timer applet when switching to a tiling wm.
#
# @note
# At this time, there is little no support for playing sound files through
# pre-packaged python3 libraries. Thus I (and any users) would have to manually
# install the libraries to use them. Thus the use of subprocess instead.
#
# @author Matthew Todd
# @date Sep 3 2011

# TODO: program options (config file?)
#   specify duration
#   specify progress bar length
#   enable/disable sound
#   specify sound volume
#   specify sound file
#   enable/disable notify-send
#   specify task (msg for notify-send)
#   specify refresh rate (sleep duration)?

import time
import sys
import os
import subprocess

notification_sound = '/usr/share/sounds/ubuntu/stereo/bell.ogg'

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

def get_message():
    '''
    Gets the completion message from the user.
    '''
    return input("Enter message: ")

def get_screen_width():
    '''
    Gets the terminal width in characters.
    '''
    info = subprocess.check_output(['stty', 'size'])
    _, screen_width = info.split()
    return int(screen_width) 

def get_progress_bar(duration, time_left, length):
    '''
    Computes the progress bar and returns it as a string.
    '''
    percentageTime = (duration - time_left) / duration
    percentageLength = int(length * percentageTime)

    return "[%s%s]" % ('='*percentageLength, '-'*(length - percentageLength))

def main():
    duration, endTime = getDuration()
    message = get_message()

    currentTime = time.time()
    while currentTime < endTime:
        currentTime = time.time()

        screen_width = get_screen_width() - 10                           # TODO: magic numbers (this one is for time remaining)

        timeLeft = endTime - currentTime

        print("%s %d \r" % (get_progress_bar(duration, timeLeft, screen_width-10), timeLeft), end="")
        sys.stdout.flush()
        time.sleep(.1)      # TODO: make sleep time dynamic?
                            # so that the progress bar is smooth (but will want to make the max 1 sec)


    print("\n%s" % message)

    # TODO: make func?
    subprocess.call(['notify-send', message])       # TODO: more informative message (get user msg?)

    # TODO: play sound
    subprocess.call(['play', '-v 100', notification_sound], stderr=subprocess.PIPE)

    return 0

if __name__ == '__main__':
    sys.exit(main())

