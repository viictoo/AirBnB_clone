#!/usr/bin/python3
"""command interpreter
"""
import cmd
from uuid import uuid4
from datetime import datetime
import sys

class print_hello(cmd.Cmd):


    def precmd(self, line):
        if not sys.stdin.isatty():
            print()
        return super().precmd(line)

    # def __str__(self):
    #     """
    #     Return string of info about model
    #     """
    #     return ('[{}] ({}) {}'.
    #             format(self.__class__.__name__, self.id, self.__dict__))

    prompt = "(hbnb) "
    def do_EOF(self, line):
        """Exit on Ctrl-D"""
        print()
        return True

    def do_quit(self, line):
        """Exit on quit. Ok Gituku!"""
        return True

    def do_printid(self, line):
        """Print UUID"""
        id = str(uuid4())
        print(id)

    def emptyline(self):
        """Overwrite default behavior to repeat last cmd"""
        pass

    def do_date(self, line):
        """print  the current cd time"""
        d_format = '%Y-%m-%dT%H:%M:%S.%f'
        created = datetime.now()
        print(created)

if __name__=="__main__":
    print_hello().cmdloop()

