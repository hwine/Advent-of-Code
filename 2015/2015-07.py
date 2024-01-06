#!/usr/bin/env python3

import cmd, sys
from turtle import *

class BobbyWiring(cmd.Cmd):
    intro = "Welcome to Bobby's wiring project.   Type help or ? to list commands.\n"
    prompt = '(bobby) '
    file = None
    wires: dict[str,int] = {}
    stack: list[str] = []

    # --- commands
    def default(self, arg:str) -> bool:
        # push first arg on stack, process rest of line

        args = arg.split()
        self.stack.append(args[0])
        print(f"pushed '{args[0]=}'")
        if len(args) > 1:
            now_do = ' '.join(args[1:])
            print(f"{now_do=}")
            return self.onecmd(now_do)
        return False

    def do_and(self, _) -> bool:
        print("do_and")
        x = self._get_int_value()
        y = self._get_int_value()
        self.stack.append(x & y)
        return False

    def do_or(self, _) -> bool:
        x = self._get_int_value()
        y = self._get_int_value()
        self.stack.append(x | y)
        return False

    def do_lshift(self, _) -> bool:
        # x LSHIFT y
        y = self._get_int_value()
        x = self._get_int_value()
        self.stack.append(x<<y)
        return False

    def do_rshift(self, _) -> bool:
        # x RSHIFT y
        y = self._get_int_value()
        x = self._get_int_value()
        self.stack.append(x>>y)
        return False

    def do_not(self, _) -> bool:
        x = self._get_int_value()
        self.stack.append(~x)
        return False

    def do_send_to(self, _) -> bool:
        print("do_send_to")
        # x -> y ==> wires[y]=x
        y = self.stack.pop()
        x = self._get_int_value()
        assert not y.isnumeric()
        assert isinstance(x, int)
        self.wires[y] = x
        return False

    def do_show(self, _) -> bool:
        for k, v in self.wires.items():
            print(f"wire '{k}' has value {v}")
        return False

    def do_eof(self, _) -> bool:
        self.do_show(_)
        return True

    # --- utilities
    def _get_int_value(self) -> int:
        # get top of stack's value. If not numeric, then it's a wire reference
        x = self.stack.pop()
        if x.isnumeric():
            return int(x)
        else:
            return int(self.wires[x])


    # --- convert infix to postfix notation
    def precmd(self, line: str) -> str:
        if not line:
            #
            return self.emptyline()
        line = line.lower()
        args = line.split()
        if len(args) >= 3 and args[-2] == "->":
            args[-2] = "send_to"
        if args[0] == "not":
            # NOT is the only unary operator, and precedence is highest
            args[1] += " " + args[0]
            del args[0]
        rewritten = ' '.join(self.postfix(args))
        print(f"{rewritten=}")
        return rewritten
    
    def postfix(self, args: list[str]) -> list[str]:
        if len(args) == 3:
            # a OP b => a b OP
            return [args[0], args[2], args[1]]
        elif len(args) > 3:
            new_first_arg = ' '.join(self.postfix(args[:3]))
            return self.postfix([new_first_arg, *args[3:]])
        else:
            return args
    def postcmd(self, stop: bool, line: str) -> bool:
        if len(self.stack):
            print(f"{len(self.stack)} items left on stack")
            print(f"{self.stack=}")
            self.stack = []
        return stop

class TurtleShell(cmd.Cmd):
    intro = 'Welcome to the turtle shell.   Type help or ? to list commands.\n'
    prompt = '(turtle) '
    file = None

    # ----- basic turtle commands -----
    def do_forward(self, arg):
        'Move the turtle forward by the specified distance:  FORWARD 10'
        forward(*parse(arg))
    def do_right(self, arg):
        'Turn turtle right by given number of degrees:  RIGHT 20'
        right(*parse(arg))
    def do_left(self, arg):
        'Turn turtle left by given number of degrees:  LEFT 90'
        left(*parse(arg))
    def do_goto(self, arg):
        'Move turtle to an absolute position with changing orientation.  GOTO 100 200'
        goto(*parse(arg))
    def do_home(self, arg):
        'Return turtle to the home position:  HOME'
        home()
    def do_circle(self, arg):
        'Draw circle with given radius an options extent and steps:  CIRCLE 50'
        circle(*parse(arg))
    def do_position(self, arg):
        'Print the current turtle position:  POSITION'
        print('Current position is %d %d\n' % position())
    def do_heading(self, arg):
        'Print the current turtle heading in degrees:  HEADING'
        print('Current heading is %d\n' % (heading(),))
    def do_color(self, arg):
        'Set the color:  COLOR BLUE'
        color(arg.lower())
    def do_undo(self, arg):
        'Undo (repeatedly) the last turtle action(s):  UNDO'
    def do_reset(self, arg):
        'Clear the screen and return turtle to center:  RESET'
        reset()
    def do_bye(self, arg):
        'Stop recording, close the turtle window, and exit:  BYE'
        print('Thank you for using Turtle')
        self.close()
        bye()
        return True

    # ----- record and playback -----
    def do_record(self, arg):
        'Save future commands to filename:  RECORD rose.cmd'
        self.file = open(arg, 'w')
    def do_playback(self, arg):
        'Playback commands from a file:  PLAYBACK rose.cmd'
        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())
    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line
    def close(self):
        if self.file:
            self.file.close()
            self.file = None

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == '__main__':
    BobbyWiring().cmdloop()
