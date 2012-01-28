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
#
# TODO: change terminal title to that of the timer message?
#       ex: "timer: laundry"
#
# TODO: include default timer sound in repo
#   create a custom one?
#       choose a file format that's likely to be playable on all linux machines by default
#
# TODO: esc/q quits program while in countdown
#   so user doesn't have to ctrl-c


import time
import sys
import os
import subprocess

notification_sound = '/usr/share/sounds/ubuntu/stereo/bell.ogg'

DEFAULT_WIDTH_OFFSET = 10

def getDuration():
    '''
    Gets the input from the user regarding the timer's duration/end time.
    @return (duration, endtime)
    '''
    done = False
    while not done:
        duration = input("Enter timer duration (in secs): ")        # TODO: handle other time formats
                                                                    # will likely need to use a parse (e.g: PLY)
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
    percentageTime = min(1.0, (duration - time_left) / duration)
    percentageLength = int(length * percentageTime)
    rest = length - percentageLength

    progress_bar = "[%s%s]" % ('='*percentageLength, '-'*rest)
    return progress_bar

def main():
    duration, endTime = getDuration()
    message = get_message()
    clear_line_terminal_code = "\033[2K"        # terminal code to clear line, b/c the number counts down, thus is shorter

    currentTime = time.time()
    width_offset = DEFAULT_WIDTH_OFFSET
    while currentTime < endTime:
        currentTime = time.time()

        timeLeft = endTime - currentTime

        screen_width = get_screen_width() - width_offset

        print("%s\r%s %d" % (clear_line_terminal_code, get_progress_bar(duration, timeLeft, screen_width), timeLeft), end="")
        sys.stdout.flush()
        time.sleep(.1)      # TODO: make sleep time dynamic?
                            # so that the progress bar is smooth (but will want to make the max 1 sec)


    print("\n%s" % message)

    # TODO: make func?
    # use PIPE to hide stderr output
    subprocess.call(['notify-send', message], stderr=subprocess.PIPE)

    # TODO: play sound
    subprocess.call(['play', '-v 100', notification_sound], stderr=subprocess.PIPE)

    return 0

if __name__ == '__main__':
    sys.exit(main())

