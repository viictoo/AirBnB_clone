#!/usr/bin/python3
"""entry point of the command interpreter
"""
import re
import ast
import cmd
import sys
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    '''command interpreter'''
    prompt = "(hbnb) "
    classes = {"BaseModel", "Amenity", "Place", "Review", "User",
               "State", "City"}

    def precmd(self, line: str) -> str:
        '''non interactive mode'''
        if not sys.stdin.isatty():
            print()
        return super().precmd(line)

    def do_EOF(self, line):
        """Ctrl-D to Exit
        """
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Override repeat last cmd"""
        pass

    def do_create(self, input):
        """Creates a new instance of BaseModel, saves
        it (to the JSON file) and prints the id"""
        if len(input) == 0:
            print("** class name missing **")
        elif input not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            instance = eval(input)()
            instance.save()
            print(instance.id)

    def do_show(self, input):
        """Prints the string representation of an instance
        based on the class name and id"""
        if len(input) == 0:
            print("** class name missing **")
        else:
            commands = tuple(input.split())
            if commands[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
            else:
                try:
                    if commands[1]:
                        insta = f'{commands[0]}.{commands[1]}'
                        if insta not in storage.all().keys():
                            print("** no instance found **")
                        else:
                            print(storage.all()[insta])
                except Exception:
                    print("** instance id missing **")

    def do_destroy(self, input):
        """Deletes an instance based on the class name and id"""
        if len(input) == 0:
            print("** class name missing **")
        else:
            commands = tuple(input.split())
            if commands[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
            else:
                try:
                    if commands[1]:
                        insta = f'{commands[0]}.{commands[1]}'
                        if insta not in storage.all().keys():
                            print("** no instance found **")
                        else:
                            del storage.all()[insta]
                            storage.save()
                except Exception:
                    print("** instance id missing **")

    def do_update(self, input):
        """Updates an instance based on the class name and id
        by adding or updating attribute"""
        if type(input) == str:
            arg_list = str.split(input)
        elif type(input) == list:
            arg_list = input
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
            key = "{}.{}".format(arg_list[0], arg_list[1])
            var_type = type(eval(arg_list[3]))
            arg3 = arg_list[3]
            arg3 = arg3.strip('"')
            arg3 = arg3.strip("'")
            try:
                if hasattr(eval(f'{arg_list[0]}'), f'{strip_(arg_list[2])}'):
                    cast_ = type(eval(f'{arg_list[0]}.{strip_(arg_list[2])}'))
                    arg3 = cast_(arg3)
            except (ValueError, TypeError, KeyError):
                arg3 = var_type(arg3)
            try:
                setattr(storage.all()[key], arg_list[2], arg3)
                storage.all()[key].save()
            except Exception:
                print("** no instance found **")

    def do_all(self, input):
        """Deletes an instance based on the class name and id"""
        str_all = []
        commands = input.split()
        if len(input) == 0:
            for insta in storage.all().values():
                str_all.append(f'{insta}')
            print(str_all)
        elif commands[0] in HBNBCommand.classes:
            for key, obj in storage.all().items():
                if commands[0] in key:
                    str_all.append(f'{obj}')
            print(str_all)
        else:
            print("** class doesn't exist **")

    def default(self, input):
        """Handle User.all() command"""
        if re.match(r'^(\S+)\.all\(.*\)$', input):
            match = re.match(r'^(\S+)\.all\(.*\)$', input)
            class_name = match.group(1)
            self.do_all(class_name)

        elif re.match(r'^(\S+)\.count\(\)$', input):
            match = re.match(r'^(\S+)\.count\(\)$', input)
            class_name = match.group(1)
            if (class_name) not in self.classes:
                print("** class doesn't exist **")
                return False
            self.insta_count(class_name)

        # elif re.match(r'^(\S+)\.show\("?(.+)"?\)$', input):
        #     match = re.match(r'^(\S+)\.show\("?(.+)"?\)$', input)
        #     class_name = strip_(match.group(1))
        #     instance_id = strip_(match.group(2))
        #     command = f'{class_name} {instance_id}'
        #     self.do_show(command)
        # elif re.match(r'^(\S+)\.destroy\("?(.+)"?\)$', input):
        #     match = re.match(r'^(\S+)\.destroy\("?(.+)"?\)$', input)
        #     class_name = match.group(1)
        #     instance_id = match.group(2)
        #     command = f'{class_name} {instance_id}'
        #     self.do_destroy(command)

        elif re.match(r'^(\S+)\.(destroy|show)\("?(.+)"?\)$', input):
            match = re.match(r'^(\S+)\.(destroy|show)\("?(.+)"?\)$', input)
            # print(match.group(1))
            # print(match.group(2))
            # print(match.group(3))
            class_name = match.group(1)
            command = match.group(2)
            instance_id = str(match.group(3))
            string = f'{command} {class_name} {instance_id}'
            # print(string)
            self.onecmd(string)

        elif re.match(r'^(\S+)\.update\("?(.+)"?,\s*(\{.+\})\)$', input):
            match = re.match(r'^(\S+)\.update\("?(.+)"?,\s*(\{.+\})\)$', input)
            class_name = match.group(1)
            instance_id = strip_(match.group(2))
            if len(class_name) == 0:
                print("** class name missing **")
                return
            elif strip_(class_name) not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            elif len(instance_id) == 0:
                print("** instance id missing **")
                return
            elif (f'{strip_(class_name)}.{instance_id}')\
                    not in storage.all().keys():
                print("** no instance found **")
                return
            data_str = match.group(3)
            data_dict = ast.literal_eval(data_str)
            if isinstance(ast.literal_eval(data_str), dict):
                for key, value in data_dict.items():
                    if isinstance(value, str):
                        self.do_update(f'{class_name} {instance_id}\
                                       {key} "{value}"')
                    else:
                        self.do_update(f'{class_name} {instance_id}\
                                       {key} {value}')
        elif re.match(r'^(\S+)\.update\(.+\)$', input):
            match = re.match(r'^(\S+)\.update\((.+)\)$', input)
            arg_list = []
            class_name = match.group(1)
            arg_list.append(class_name)
            attributes = match.group(2)
            attributes = attributes.split(', ')
            if class_name:
                arg_list += attributes
            if check_update(arg_list):
                for i in range(3):
                    arg_list[i] = strip_(arg_list[i])
                self.do_update(arg_list)
        else:
            print(f"*** Unknown syntax: {input}")

    def insta_count(self, input):
        """count instances"""
        instas = storage.all()
        count = 0
        for inst in instas:
            if input == instas[inst].to_dict()["__class__"]:
                count += 1
        print(count)


def strip_(input):
    """remove enclosing quoutes"""
    sample = input.strip('"')
    sample = sample.strip("'")
    return sample


def check_update(input):
    """check string syntax"""
    arg_list = input
    if len(arg_list) == 0:
        print("** class name missing **")
    elif strip_(arg_list[0]) not in HBNBCommand.classes:
        print("** class doesn't exist **")
    elif len(arg_list) == 1:
        print("** instance id missing **")
    elif (f"{strip_(arg_list[0])}.{strip_(arg_list[1])}") not in \
            storage.all().keys():
        print("** no instance found **")
    elif len(arg_list) == 2:
        print("** attribute name missing **")
    elif len(arg_list) == 3:
        print("** value missing **")
    else:
        return True
    return False


if __name__ == "__main__":
    HBNBCommand().cmdloop()
