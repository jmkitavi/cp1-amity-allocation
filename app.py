'''
Usage:
    add_person <first_name> <last_name> <role> [--wants_accomodation=N]
    create_room <room_name> <room_type>
    reallocate_person <full_name> <new_room_name>
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
    --wants_accomodation=<N> [defult: N]
'''

from app.amity import Amity
import sys
import cmd
import os
import time
from termcolor import cprint, colored
from pyfiglet import figlet_format
from docopt import docopt, DocoptExit


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

            print('Invalid Command!')
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


# def save_state_on_interrupt():
#     time_stamp = time.strftime("%Y-%m-%d-%H:%M")
#     db_name = "backup-at-" + time_stamp
#     print("Saving state to " + db_name)
#     Amity.save_state(db_name)


class AmityApplication(cmd.Cmd):
    amity = Amity()

    # cprint(figlet_format('AMITY', font='banner3-D'), 'cyan', attrs=['bold'])

    prompt = "(amity)"

    @docopt_cmd
    def do_create_room(self, arg):
        '''Usage: create_room <room_name> <room_type>'''
        room_name = arg["<room_name>"]
        room_type = arg["<room_type>"]
        self.amity.create_room(room_name, room_type)

    @docopt_cmd
    def do_add_person(self, arg):
        '''Usage: add_person <first_name> <last_name> <role> [accomodation]'''
        first_name = arg["<first_name>"]
        last_name = arg["<last_name>"]
        role = arg["<role>"]
        accomodation = arg["accomodation"]
        if accomodation is None:
            accomodation = "N"
        self.amity.add_person(first_name, last_name, role, accomodation=accomodation)

    @docopt_cmd
    def do_reallocate_person(self, arg):
        '''Usage: reallocate_person <first_name> <last_name> <room_name>'''
        first_name = arg["<first_name>"]
        last_name = arg["<last_name>"]
        room_name = arg["<room_name>"]
        self.amity.reallocate_person(first_name, last_name, room_name)

    @docopt_cmd
    def do_load_people(self, arg):
        '''Usage: load_people <file_name>'''
        file_name = arg["<file_name>"]
        self.amity.load_people(file_name)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        '''Usage: print_unallocated [--o=file_name]'''
        file_name = arg["--o"] or None
        self.amity.print_unallocated(file_name)

    @docopt_cmd
    def do_print_room(self, arg):
        '''Usage: print_room <room_name>'''
        room_name = arg["<room_name>"]
        self.amity.print_room(room_name)

    @docopt_cmd
    def do_print_people(self, arg):
        '''Usage: print_people'''
        self.amity.print_people()

    @docopt_cmd
    def do_print_allocations(self, arg):
        '''Usage: print_allocations [--o=file_name]'''
        file_name = arg["--o"] or None
        self.amity.print_allocations(file_name)

    @docopt_cmd
    def do_load_state(self, arg):
        '''Usage: load_state <database>'''
        database = arg["<database>"]
        self.amity.load_state(database)

    @docopt_cmd
    def do_save_state(self, arg):
        '''Usage: save_state <database>'''
        database = arg["<database>"]
        self.amity.save_state(database)

    @docopt_cmd
    def do_quit(self, arg):
        '''Usage: quit'''
        exit()

if __name__ == '__main__':
    introduction()
    try:
        AmityApplication().cmdloop()
    except KeyboardInterrupt:
        time_stamp = time.strftime("%Y-%m-%d-%H:%M")
        db_name = "backup-at-" + time_stamp
        print("\nKeyBoardInterrupt!!\nSaving state to " + db_name + "\n")
        AmityApplication.amity.save_state(db_name)