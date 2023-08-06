#!/usr/bin/python3
"""entry point of the command interpreter
"""
import cmd
import sys
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    '''command interpreter'''
    prompt = "(hbnb) "
    classes = {"BaseModel"}

    def precmd(self, line: str) -> str:
        '''non interactive mode
        '''
        if not sys.stdin.isatty():
            print()
        return super().precmd(line)

    def do_EOF(self, line):
        """Ctrl-D to Exit
        """
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program
        """
        return True

    def emptyline(self):
        """Override repeat last cmd
        """
        pass

    def do_create(self, input):
        """Creates a new instance of BaseModel, saves
        it (to the JSON file) and prints the id"""
        if len(input) == 0:
            print("** class name missing **")
        elif input not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            # print(input)
            # instance = input() TypeError: 'str' object is not callable
            instance = eval(input)()
            instance.save()
            print(instance.id)

    def do_show(self, input):
        """Prints the string representation of an instance
        based on the class name and id
        """
        if len(input) == 0:
            print("** class name missing **")
        else:
            commands = tuple(input.split())
            # print(commands[0])
            if commands[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
            else:
                try:
                    if commands[1]:
                        # print(commands[1])
                        insta = f'{commands[0]}.{commands[1]}'
                        if insta not in storage.all().keys():
                            print("** no instance found **")
                        else:
                            print(storage.all()[insta])
                except Exception:
                    print("** instance id missing **")

                # print(storage.all())
    def do_destroy(self, input):
        """Deletes an instance based on the class name and id"""
        if len(input) == 0:
            print("** class name missing **")
        else:
            commands = tuple(input.split())
            # print(commands[0])
            # print("----")
            if commands[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
            else:
                try:
                    if commands[1]:
                        # print(commands[1])
                        insta = f'{commands[0]}.{commands[1]}'
                        if insta not in storage.all().keys():
                            print("** no instance found **")
                        else:
                            print(storage.all()[insta])
                            del storage.all()[insta]
                            storage.save()
                except Exception:
                    print("** instance id missing **")

    def do_update(self, input):
        """Updates an instance based on the class name and id
        by adding or updating attribute
        """
        arg_list = str.rsplit(input)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif (f"{arg_list[0]}.{arg_list[1]}") not in storage.all().keys():
            print("** no instance found **")
        elif len(arg_list) == 2:
            print("** attribute name missing **")
        elif len(arg_list) == 3:
            print("** value missing **")
        elif len(arg_list) >= 4:
            print(arg_list)
            key = "{}.{}".format(arg_list[0], arg_list[1])
            # print(key)
            cast = type(eval(arg_list[3]))
            # print(cast)
            arg3 = arg_list[3]
            # print(arg3)
            arg3 = arg3.strip('"')
            arg3 = arg3.strip("'")
            # print(arg3)
            try:
                setattr(storage.all()[key], arg_list[2], cast(arg3))
                storage.all()[key].save()
            except Exception:
                print("** no instance found **")

    def do_all(self, input):
        """Deletes an instance based on the class name and id"""
        str_all = []
        if len(input) == 0:
            for insta in storage.all().values():
                # print(insta)
                str_all.append(f'{insta}')
            print(str_all)
        else:
            commands = tuple(input.split())
            # print(commands[0])
            # print("----")
            if commands[0] in HBNBCommand.classes:
                for key, obj in storage.all().items():
                    if commands[0] in key:
                        str_all.append(f'{obj}')
                        # print(obj)
                        print(str_all)
            else:
                print("** class doesn't exist **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
