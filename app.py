"""
Usage:
    add_person <first_name> <last_name> <role> [--a=N]
    create_room <room_name> <room_type>
    allocate <first_name> <last_name> <room_name>
    reallocate_person <first_name> <last_name> <new_room_name>
    load_people <filename>
    print_people
    print_allocations [--o=filename]
    print_unallocated [--o=filename]
    print_room <room_name>
    save_state <database>
    load_state <database>
    quit
Options:
    -h, --help  Show this screen and exit
    -i --interactive  Interactive Mode
    wants_accomodation --a=<N> [defult: N]
"""

import sys
import cmd
import os
import time
from termcolor import colored
from docopt import docopt, DocoptExit
from app.amity import Amity


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print(colored("Invalid Command!", "red"))
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

border = colored("*" * 20, 'red').center(80)


def introduction():
    print(border)
    print("AMITY SPACE ALLOCATION!".center(70))
    print(__doc__)
    print(border)


class AmityApplication(cmd.Cmd):
    amity = Amity()

    prompt = "(amity)"

    @docopt_cmd
    def do_create_room(self, arg):
        """
        Creates a room(s) in amity
        Usage: create_room <room_type> <room_name>  ...
        """
        room_type = arg["<room_type>"]
        for name in arg['<room_name>']:
            print(self.amity.create_room(room_type, name))
        print("\n")

    @docopt_cmd
    def do_add_person(self, arg):
        """
        Add new people to amity. Fellows and Staff
        Usage: add_person <firstname> <lastname> <role> [--a=N]
        """
        first_name = arg["<firstname>"]
        last_name = arg["<lastname>"]
        role = arg["<role>"]
        wants_accomodation = arg["--a"]
        print(self.amity.add_person(first_name, last_name, role, str(wants_accomodation)))
        print("\n")

    @docopt_cmd
    def do_allocate(self, arg):
        """
        Allocates someone in unallocated a room
        Usage: allocate <first_name> <last_name> <room_name>
        """
        first_name = arg["<first_name>"]
        last_name = arg["<last_name>"]
        room_name = arg["<room_name>"]
        print(self.amity.allocate(first_name, last_name, room_name))
        print("\n")

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """
        Re-allocates someone from one room to another
        Usage: reallocate_person <first_name> <last_name> <room_name>
        """
        first_name = arg["<first_name>"]
        last_name = arg["<last_name>"]
        room_name = arg["<room_name>"]
        print(self.amity.reallocate_person(first_name, last_name, room_name))
        print("\n")

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <file_name>"""
        file_name = arg["<file_name>"]
        self.amity.load_people(file_name)
        print("\n")

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=file_name]"""
        file_name = arg["--o"] or None
        self.amity.print_unallocated(file_name)
        print("\n")

    @docopt_cmd
    def do_print_room(self, arg):
        """
        Prints occupants in a room
        Usage: print_room <room_name>
        """
        room_name = arg["<room_name>"]
        print(self.amity.print_room(room_name))
        print("\n")

    @docopt_cmd
    def do_print_people(self, arg):
        """
        Print all people in amity. Fellows and Staff
        Usage: print_people
        """
        print(self.amity.print_people())
        print("\n")

    @docopt_cmd
    def do_print_allocations(self, arg):
        """
        Prints out allocations to scree and option file
        Usage: print_allocations [--o=file_name]
        """
        file_name = arg["--o"] or None
        print(self.amity.print_allocations(file_name))
        print("\n")

    @docopt_cmd
    def do_load_state(self, arg):
        """
        Loads amity state from a database
        Usage: load_state <database>
        """
        database = arg["<database>"]
        print(self.amity.load_state(database))
        print("\n")

    @docopt_cmd
    def do_save_state(self, arg):
        """
        Saves amity state to a database
        Usage: save_state <database>
        """
        database = arg["<database>"]
        print(self.amity.save_state(database))
        print("\n")

    @docopt_cmd
    def do_quit(self, arg):
        """
        Exits Amity
        Usage: quit
        """
        print(colored("The derp is strong with this one".center(40), "red"))
        print("GOOD BYE!!".center(30))
        exit()

if __name__ == '__main__':
    introduction()
    try:
        AmityApplication().cmdloop()
    except KeyboardInterrupt:
        time_stamp = time.strftime("%Y-%m-%d-%H:%M")
        db_name = "backup-at-{0}".format(time_stamp)
        print("\nKeyBoardInterrupt!!\nSaving state to {0} \n".format(db_name))
        AmityApplication.amity.save_state(db_name)
