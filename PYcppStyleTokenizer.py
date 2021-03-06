#
# this is an extension of:
# https://docs.python.org/3.2/library/re.html#writing-a-tokenizer
#

import collections
import re

#strucure returned by 'tokenize'
Token = collections.namedtuple('Token', [
 'typ',         #name of type
 'value',       #string form imput
 'line',        #line mumber (0..n)
 'column',      #column in line (0...n)
 'blockDepth',  # {} block depth
 'argDepth',    # () arguments depth
 'arrDepth',    # [] array depth
]) 

def tokenize(input,visibleNewLine=False):
    keywords      = {'if', 'private', 'for', 'while', 'return'}
    keywordsTypes = {'void', 'int','float'}

    #token names starting with _ are not returned
    token_specification = [
        ('NUMBER',     r'\d+(\.\d*)?'),    # Integer or decimal number
        ('ASSIGN',     r'='),              # Assignment operator
        ('END',        r';'),              # Statement terminator
        ('NEXT',       r','),              # Argumnet separator
        ('BLOCKSTART', r'{'),              # Start of new block of code (has depth)
        ('BLOCKEND',   r'}'),              # End of block of code
        ('ARGSTART',   r'\('),             # Start of new agrument block (has depth)
        ('ARGEND',     r'\)'),             # End of argument block
        ('ARRSTART',   r'\['),             # Start of array block (has depth)
        ('ARREND',     r'\]'),             # End of array block
        ('STRING',     r'"([^"\\]|\\.)*"'),# String (can contain quotes)
        ('ID',         r'[A-Za-z][\w]*'),  # Identifiers
        ('COMMENT1',   r'\/\/[^\n]*'),     # single line comment
        ('COMMENT2',   r'/\*.*?\*/'),      # multiline comment
        ('OP',         r'[+*\/\-]'),       # Arithmetic operators
        ('CMP',        r'[\<\>]\=?'),      # Comparators <,>,<=,>=
        ('NL',         r'\n'),             # Line endings
        ('SKIP',       r'[ \t]')           # Skip over spaces and tabs
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification) #join all into one regexp
    get_token = re.compile(tok_regex,re.DOTALL).match #comile rexexp. '.' can be newnline

    line = pos = line_start = depth = arg = arr =  0 #values for while loop all 0

    mo = get_token(input)
    while mo is not None:
      typ = mo.lastgroup
      val = mo.group(typ)

      if typ != 'SKIP':
        if   typ == 'BLOCKSTART': depth+=1
        elif typ == 'ARGSTART':   arg+=1
        elif typ == 'ARRSTART':   arr+=1

        if visibleNewLine or typ != 'NL': #hide new line is requested
          if typ == 'ID' and val in keywords: #translate ID to 'KEYWORD'
            typ = 'KEYWORD'
          elif  typ == 'ID' and val in keywordsTypes: #translate ID to 'TYPE'
            typ = 'TYPE'
          yield Token(typ, val, line, mo.start()-line_start,depth,arg,arr) #add new token

        if typ == 'NL':
          line_start = mo.start()+1 
          line += 1

        if   typ == 'BLOCKEND': depth-=1
        elif typ == 'ARGEND':   arg-=1
        elif typ == 'ARREND':   arr-=1
        elif typ == 'COMMENT2': line+=val.count("\n")

      #if skip
      pos = mo.end()
      mo = get_token(input, pos)
    #while
    if pos != len(input):
        raise RuntimeError('Unexpected character %r on line %d' %(input[pos], line))
