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
            # print(input)
            # instance = input() TypeError: 'str' object is not callable
            # eval = execute line of code
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

    def do_destroy(self, input):
        """Deletes an instance based on the class name and id"""
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
                            del storage.all()[insta]
                            storage.save()
                except Exception:
                    print("** instance id missing **")

    def do_update(self, input):
        # print(input)
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
            # print(arg_list)
            key = "{}.{}".format(arg_list[0], arg_list[1])
            # print(key)
            var_type = type(eval(arg_list[3]))
            # print("----")
            # print(var_type)
            # print("----")
            arg3 = arg_list[3]
            # if cast is float:
            #     arg3 = round(arg3, 1)
            # print(arg3)
            arg3 = arg3.strip('"')
            arg3 = arg3.strip("'")
            # print(arg3)
            try:
                setattr(storage.all()[key], arg_list[2], var_type(arg3))
                storage.all()[key].save()
            except Exception:
                print("** no instance found **")

    def do_all(self, input):
        """Deletes an instance based on the class name and id"""
        str_all = []
        # commands = tuple(input.split())
        commands = input.split()
        if len(input) == 0:
            for insta in storage.all().values():
                # print(insta)
                str_all.append(f'{insta}')
                # str_all.append(insta)
            print(str_all)
        elif commands[0] in HBNBCommand.classes:
            for key, obj in storage.all().items():
                if commands[0] in key:
                    str_all.append(f'{obj}')
                    # str_all.append(obj)
                    # print(obj)
            print(str_all)
        else:
            print("** class doesn't exist **")

    def default(self, input):
        """Handle User.all() command"""
        # if input.endswith('.all()'):
        # print(input)
        if re.match(r'^(\S+)\.all\(.*\)$', input):
            match = re.match(r'^(\S+)\.all\(.*\)$', input)
            class_name = match.group(1)
            self.do_all(class_name)
            # print(input[:-6])
            # HBNBCommand.do_all(self, input)
        # elif input.endswith('.count()'):
        # elif re.match(r'^(.+)\.count\("?(.*)"?\)$', input):
        elif re.match(r'^(\S+)\.count\(\)$', input):
            match = re.match(r'^(\S+)\.count\(\)$', input)
            class_name = match.group(1)
            if (class_name) not in self.classes:
                print("** class doesn't exist **")
                return False
            self.insta_count(class_name)
            # print(input[:-6])
            # HBNBCommand.do_all(self, input)
        elif re.match(r'^(\S+)\.show\("?(.+)"?\)$', input):
            match = re.match(r'^(\S+)\.show\("?(.+)"?\)$', input)
            class_name = my_strip(match.group(1))
            instance_id = my_strip(match.group(2))
            # print(f"destroy {class_name} {instance_id}")
            command = f'{class_name} {instance_id}'
            self.do_show(command)
        elif re.match(r'^(\S+)\.destroy\("?(.+)"?\)$', input):
            match = re.match(r'^(\S+)\.destroy\("?(.+)"?\)$', input)
            class_name = match.group(1)
            instance_id = match.group(2)
            # print(f"destroy {class_name} {instance_id}")
            command = f'{class_name} {instance_id}'
            self.do_destroy(command)
        # elif re.match(r'^(.*)\.update\("(.*)"\)$', input):
        #     match = re.match(r'^(.*)\.update\((.*)\)$', input)
        #     class_name = match.group(1)
        #     info = match.group(2)
        #     info = info.split(',')
            # info = info.strip('"')
            # info = info.strip("'")
            # print(info)
            # print(f"destroy {class_name} {instance_id}")
            # command = f'{class_name} {info}'
            # self.do_update(command)
        # elif re.match(r'^(\w+)\.update\("(.+)",
        # "([^"]+)", "([^"]+)"\)$', input):
        elif re.match(r'^(\S+)\.update\("?(.+)"?,\s*(\{.+\})\)$', input):
            match = re.match(r'^(\S+)\.update\("?(.+)"?,\s*(\{.+\})\)$', input)
            class_name = match.group(1)
            instance_id = my_strip(match.group(2))
            # if (instance_id) not in storage.all().keys():
            #     print("** no instance found **")
            #     return
            if len(class_name) == 0:
                print("** class name missing **")
                return
            elif my_strip(class_name) not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            elif len(instance_id) == 0:
                print("** instance id missing **")
                return
            elif (f'{my_strip(class_name)}.{instance_id}')\
                    not in storage.all().keys():
                print("** no instance found **")
                return
            # print(type(match.group(3)))
            data_str = match.group(3)
            data_dict = ast.literal_eval(data_str)
            # check if input is indeed a dictionary
            if isinstance(ast.literal_eval(data_str), dict):
                for key, value in data_dict.items():
                    if isinstance(value, str):
                        # print(f'{class_name} {instance_id} {key} "{value}"')
                        self.do_update(f'{class_name} {instance_id}\
                                       {key} "{value}"')
                    else:
                        # print(f'{class_name} {instance_id} {key} {value}')
                        self.do_update(f'{class_name} {instance_id}\
                                       {key} {value}')
            # updates = " ".join([f"{key} {value}" for key,
            # value in data_dict.items()])
            # print(f"{class_name} {instance_id}  {updates}")
        elif re.match(r'^(\S+)\.update\(.+\)$', input):
            # match = re.match(r'^(\w+)\.update\("(.+)",
            # "([^"]+)","([^"]+)"\)$',input)
            match = re.match(r'^(\S+)\.update\((.+)\)$', input)
            # class_name = match.group(1)
            arg_list = []
            class_name = match.group(1)
            arg_list.append(class_name)
            attributes = match.group(2)
            attributes = attributes.split(', ')
            if class_name:
                arg_list += attributes
            # print(arg_list)
            if check_update(arg_list):
                for i in range(3):
                    arg_list[i] = my_strip(arg_list[i])
                # print(arg_list)
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


def my_strip(input):
    """remove enclosing quoutes"""
    sample = input.strip('"')
    sample = sample.strip("'")
    return sample


def check_update(input):
    """check string syntax"""
    arg_list = input
    if len(arg_list) == 0:
        print("** class name missing **")
    elif my_strip(arg_list[0]) not in HBNBCommand.classes:
        print("** class doesn't exist **")
    elif len(arg_list) == 1:
        print("** instance id missing **")
    elif (f"{my_strip(arg_list[0])}.{my_strip(arg_list[1])}") not in \
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
