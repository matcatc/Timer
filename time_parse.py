#!/usr/bin/python3
'''
Parses time durations.

Because PLY uses bottom up parsers, can't do stuff like OPT_X OPT_Y b/c OPT_X
will eat up NUMBER's that belong to Y. This is due to limited token look ahead.
But the current implementation is better because it works and is also more
flexible with input (doesn't have to be in a specific order.)

Because its unclear how many days should be in a month, its not included.

@date Mar 23, 2012
@author Matthew Todd
'''

YEAR_ID     = 'year'
MONTH_ID    = 'month'
WEEK_ID     = 'week'
DAY_ID      = 'day'
HOUR_ID     = 'hour'
MIN_ID      = 'min'
SEC_ID      = 'sec'


import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from time_lex import tokens


start = 'start'

def p_start(p):
    'start : time_duration'
    p[0] = p[1]


# returns a dict of unit_type -> value
def p_time_duration(p):
    '''
    time_duration  : time_duration year
                   | time_duration week
                   | time_duration day
                   | time_duration hour
                   | time_duration min
                   | time_duration sec
                   | empty
    '''
    p[0] = p[1]
    if p[0] is None:
        p[0] = {YEAR_ID:0, WEEK_ID:0, DAY_ID:0, HOUR_ID:0, MIN_ID:0, SEC_ID:0}

    if len(p) > 2:
        key, value = p[2]
        p[0][key] = value


def p_year(p):
    'year : NUMBER YEAR'
    p[0] = (YEAR_ID, p[1])


def p_month(p):
    'month : NUMBER MONTH'
    p[0] = (MONTH_ID, p[1])


def p_week(p):
    'week : NUMBER WEEK'
    p[0] = (WEEK_ID, p[1])


def p_day(p):
    'day : NUMBER DAY'
    p[0] = (DAY_ID, p[1])


def p_hour(p):
    'hour : NUMBER HOUR'
    p[0] = (HOUR_ID, p[1])


def p_min(p):
    'min : NUMBER MIN'
    p[0] = (MIN_ID, p[1])


def p_sec(p):
    'sec : NUMBER SEC'
    p[0] = (SEC_ID, p[1])


def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!\n\t%r" % p)


# Build the parser
parser = yacc.yacc()


def main():
    while True:
       try:
           s = input('input > ')
       except EOFError:
           break
       if not s: continue
       result = parser.parse(s)
       print(result)
    print("\n")

if __name__ == '__main__':
    main()

