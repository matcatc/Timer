#!/usr/bin/python3
'''
Simple (hopefully) script to do countdown timer stuff. Created to fill the
void left by gnome's timer applet when switching to a tiling wm.

@note
At this time, there is little no support for playing sound files through
pre-packaged python3 libraries. Thus I (and any users) would have to manually
install the libraries to use them. Thus the use of subprocess instead.

@author Matthew Todd
@date Sep 3 2011

TODO: program options (config file?)
  specify duration
  specify progress bar length
  enable/disable sound
  specify sound volume
  enable/disable notify-send
  specify task (msg for notify-send/espeak)
  specify refresh rate (sleep duration)?

TODO: change terminal title to that of the timer message?
      ex: "timer: laundry"

TODO: esc/q quits program while in countdown
  so user doesn't have to ctrl-c

TODO: output in mixed unit formats
  Can also use timedelta to output time left w/ mixed units (will need to do a little math).

TODO: input duration grammar for docs
  So users can know valid input grammar info.
  Low priority, should be obvious enough that users don't need to be told explicitly. Tech-savy users can just look at the grammar.

TODO: input end time instead of time duration
  Will want to use command line switch?
  Can build into grammar instead.
'''


import time
import sys
import os
import subprocess
from datetime import timedelta

try:
    import time_parse
    time_parse_enabled = True
except Exception as e:
    print('Failed to import time_parse(%s), defaulting to seconds only input' % e)
    time_parse_enabled = False
    

DEFAULT_WIDTH_OFFSET = 10


def getDuration():
    '''
    Gets the input from the user regarding the timer's duration/end time.

    Uses time_parse so that user can input different time units.

    @return (duration, endtime)
    '''
    done = False
    while not done:
        try:
            duration = input("Enter timer duration: ")

            if(time_parse_enabled):
                result = time_parse.parser.parse(duration)

                week = 52*result[time_parse.YEAR_ID] + result[time_parse.WEEK_ID]
                delta = timedelta(weeks=week,
                                    days=result[time_parse.DAY_ID],
                                    hours=result[time_parse.HOUR_ID],
                                    minutes=result[time_parse.MIN_ID],
                                    seconds=result[time_parse.SEC_ID])

                duration = delta.total_seconds()
            else:
                duration = int(duration)

            done = True
        except EOFError:
            print("")
            sys.exit(0)
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

    # play sound
    # TODO: make func?
    subprocess.call(['espeak', '-a 200', message], stderr=subprocess.PIPE)

    return 0

if __name__ == '__main__':
    sys.exit(main())

