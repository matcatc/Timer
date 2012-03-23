#!/usr/bin/python3
'''
Tokenizer for time duration.

@date Mar 23, 2012
@author Matthew Todd
'''

import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'NUMBER',
    'YEAR',
    'MONTH',
    'WEEK',
    'DAY',
    'HOUR',
    'MIN',
    'SEC'
)

# Regular expression rules for simple tokens
# the (s){0,1}'s are there to make plural optional
t_YEAR  = r'year(s){0,1}'
t_MONTH = r'month(s){0,1}'
t_WEEK  = r'week(s){0,1}'
t_DAY   = r'day(s){0,1}'
t_HOUR  = r'hour(s){0,1}'
t_MIN   = r'(minute|min)(s){0,1}'
t_SEC   = r'(second|sec)(s){0,1}'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Ignored chars
t_ignore  = ' \t\n'

# Error handling rule
def t_error(t):
    '''
    TODO: error/exception/quit?
    '''
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


# test
def main():
    data = '''
        3 weeks 2day 17 hours 5mins 3 second
    '''

    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)

if __name__ == '__main__':
    main()

