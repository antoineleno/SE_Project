#!/usr/bin/python3
"""
console module
"""
from os import getenv
import importlib
import cmd
import sys

from models.base_model import BaseModel
from models.models import User, Program, Course
from models.models import Project, Enrollment, Resource
from models.models import Task, TaskAnswer, UserTask, Quiz
from models.models import Answer, UserQuiz



class ECOURSECommand(cmd.Cmd):
    """Console class"""
    prompt = '(RoofMarket) ' if sys.__stdin__.isatty() else ''
    classes = {
               'BaseModel': BaseModel, 'User': User, 'Program': Program,
               'Course': Course, 'Project': Project, 'Enrollment': Enrollment,
               'Resource': Resource, 'Task': Task, 'TaskAnswer': TaskAnswer,
               'UserTask': UserTask, 'Quiz': Quiz, 'Answer': Answer, 'UserQuiz': UserQuiz
              }

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Called when an empty line is entered"""
        pass

    def do_EOF(self, line):
        """Handle End-of-File (EOF) condition to exit the program gracefully"""
        print()
        return True

    def do_create(self, args):
        """ Create an object of any type

            Usage: create class_name
        """
        try:
            for i in range(1):
                arguments = shlex.split(args)
                f_arguments = arguments[1:]
                if not args:
                    print("** class doesn't exist **")
                    return
                elif arguments[0] not in ECOURSECommand.classes:
                    print("** class doesn't exist **")
                    return
                new_instance = globals()[arguments[0]]()

                for my_args in f_arguments:
                    key, value = my_args.split("=")
                    print(type(key), type(value))
                    setattr(new_instance, key, value)
                new_instance.save()
                print(new_instance.id)
        except Exception as e:
            print(e)


    def do_destroy(self, args):
        """Delete an object or row from the database
        Usage: destroy class_name object_id
        
        """
        
        arguments = shlex.split(args)
        if not args:
            print("** class doesn't exist **")
            return
        elif arguments[0] not in ECOURSECommand.classes:
            print("** class doesn't exist **")
            return
        elif len(arguments) == 1:
            print("** provide the id of the object **")
            return
        ob_id = "{}.{}".format(arguments[0].lower(), arguments[1])
        for key, value in storage.all(arguments[0]).items():
            if (key == ob_id):
                value.delete()
                storage.save()

    def do_all(self, args):  
        print(storage.get_object(User))

    def do_get(self, args):
        """Get an object"""
        if args:
            arguments = shlex.split(args)
            if len(arguments) == 2:
                user = storage.get_object(User, id="9566ffb2-1df8-496f-8f13-972bdf2f60ab")
                print(user)
                user.delete()
                storage.save()
                


if __name__ == '__main__':
    ECOURSECommand().cmdloop()
