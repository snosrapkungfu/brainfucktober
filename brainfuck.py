#!/usr/bin/python

import sys
from bfrunner import BFRunner

PROMPT = 'F8ck: '

BANNER = '''
Python Brainfuck Interpreter
------ --------- -----------

  Interpreter commands

  $help            ... reprint this banner
  $load <filename> ... load and run brainfuck file
  $core            ... dump corestore memory to screen
  $fuck            ... reset brainfuck tape
  $quit            ... exit

  Brainfuck Language

  < ... move pointer left
  > ... move pointer right
  + ... increment cell
  - ... decrement cell
  , ... read a character from user
  . ... send a character to user
  [ ... loopstart
  ] ... loopend

'''

def repl( prompt = PROMPT ):
    ''' repl loop '''

    print BANNER
    runner = BFRunner()

    while True:

        bf_command = raw_input( prompt ).strip()
        if bf_command.startswith( '$' ):
            if bf_command == '$quit':
                return
            elif bf_command == '$fuck':
                runner.initializeTape()
            elif bf_command == '$core':
                print runner.core_store
            elif bf_command == '$help':
                print BANNER
            elif bf_command.startswith( '$load' ):
                print 'todo lol'
            else:
                print 'No idea what u mean'
        else:
            runner.run( bf_command )

def main():
    repl()

if __name__ == '__main__':
    main()
