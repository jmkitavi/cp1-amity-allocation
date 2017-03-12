[![Issue Count](https://lima.codeclimate.com/github/sirjmkitavi/cp1-amity-allocation/badges/issue_count.svg)](https://lima.codeclimate.com/github/sirjmkitavi/cp1-amity-allocation)
# Checkpoint 1 - Amity Space Allocation
## Introduction
The Amity room allocation is a system that allocates rooms to the Staff and fellows working at Andela. Developed in #python.

1. `create_room <room> <room_name>(s)...` - Creates a room in Amity. This command can create as many rooms as possible by specifying multiple room names
2. `add_person <firstname> <lastname> <fellow|staff> [--a=N]` - Add a person to the system and allocates the person to a random room
3. `reallocate_person <firstname> <lastname>> <new_room_name>` - Reallocate the person to `new_room_name`
4. `allocate <firstname> <lastname> <room_name>` - Allocates someone on unallocated to a room
5. `load_people <filename>` - Adds people to rooms from a text file
6. `print_allocations [-o=filename]` - Prints a list of allocations  onto the screen. Specifying the optional -o option here outputs the information to the text file provided
7. `print_unallocated [-o=filename]` - Prints a list of unallocated people to the screen. Specifying the -o option here outputs the information to the text file provided
8. `print_room <room_name>` - Prints the names of the people in `room_name` on the screen
9. `save_state [--db=sqlite_database]` - Persists all the data stored in the app to a SQLite database. Specifying the --db parameter explicitly stores the data in the sqlite_database specified.
10. `load_state <sqlite_database>` - Loads data from a database into the application.

## Installation & Setup
1. Download & Install Python
 	* Head over to the [Python Downloads](https://www.python.org/downloads/) Site
2. Clone the repository to your personal computer to any folder
  * Url  - https://github.com/sirjmkitavi/cp1-amity-allocation
 	* Enter the terminal on Mac/Linux.
 	* Type `git clone ` and paste the URL
