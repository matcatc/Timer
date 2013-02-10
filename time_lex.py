#!/usr/bin/python3
'''
Tokenizer for time duration.


@license
    This file is part of Timer.

    Timer is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Timer is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Timer.  If not, see <http://www.gnu.org/licenses/>.

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

