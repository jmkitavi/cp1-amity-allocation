"""app/amity"""
import sys
import os
import time
import sqlite3
from random import choice
from sqlalchemy import select
from app.db.database import Base, Employees, Allocations, Rooms, DatabaseCreator, Unallocated


class Amity(object):
    def __init__(self):
        self.all_people = [""]
        self.all_fellow = []
        self.all_staff = []
        self.office_waiting_list = []  # all staff without office
        self.living_space_waiting_list = []  # all fellow without living
        self.all_rooms = []
        self.all_offices = []
        self.all_living = []
        self.room_allocations = {
            "office": {},
            "living": {}}

    def create_room(self, room_name, room_type):
        room_type = room_type.upper()
        room_name = room_name.upper()
        # check if room name exists
        if room_name in self.all_rooms:
            msg = ("%s - room name already used" % room_name)
            print(msg)
            # return(msg)
        else:
            # check if room type is correct
            if room_type in ('OFFICE', 'LIVING'):
                self.all_rooms.append(room_name)

                if room_type == "OFFICE":
                    self.all_offices.append(room_name)
                    self.room_allocations["office"][room_name] = []
                    msg = ("%s - office added successfully" % room_name)
                    print(msg)
                    # return(msg)

                elif room_type == 'LIVING':
                    self.all_living.append(room_name)
                    self.room_allocations["living"][room_name] = []
                    msg = ("%s - living space added successfully" % room_name)
                    print(msg)

            else:
                print("%s is a wrong room type" % room_type)

    def add_person(self, first_name, last_name, role, accomodation="N"):
        full_name = (first_name + " " + last_name).upper()
        role = role.upper()
        accomodation = accomodation.upper()

        if full_name in self.all_people:
            print("%s already used " % full_name)
        else:
            if(role in ("FELLOW", "STAFF")):
                self.all_people.append(full_name)

                # assign random office to everyone
                office = self.select_random_office()
                if office is False:
                    self.office_waiting_list.append(full_name)
                    msg1 = "No office available at this time"
                    msg2 = "Added to waiting list"
                    o_msg = msg1 + "\n" + msg2
                else:
                    self.room_allocations["office"][office].append(full_name)
                    o_msg = "Allocated office " + office

                if role == "FELLOW":
                    self.all_fellow.append(full_name)
                    msg = ("%s - fellow added successfully" % full_name)
                    print(msg)
                    print(o_msg)

                    # if fellow accomodation is yes allocate living
                    if accomodation == "Y":
                        living = self.select_random_living()
                        if living is False:
                            self.living_space_waiting_list.append(full_name)
                            msg2 = "No Living space available at this time"
                            print(msg2)
                            print("Added to waiting list")
                        else:
                            self.room_allocations["living"][living].append(
                                full_name)
                            msg2 = "Allocated living space " + living
                            print(msg2)
                        # print(msg2)

                elif role == "STAFF":
                    self.all_staff.append(full_name)
                    msg = ("%s - staff added successfully" % full_name)
                    print(msg)
                    print(o_msg)
                    if accomodation == "Y":
                        msg2 = "Sorry! staff don't get accomodation"
                        print(msg2)

            else:
                print("Error! Please indicate correct role.\nEither Fellow or Staff")

    def select_random_office(self):
        available = []
        for office in self.all_offices:
            if len(self.room_allocations["office"][office]) < 6:
                available.append(office)
        if len(available) < 1:
            return False
        office = choice(available)
        return office

    def select_random_living(self):
        available = []
        for living in self.all_living:
            if len(self.room_allocations["living"][living]) < 4:
                available.append(living)
        if len(available) < 1:
            return False
        living = choice(available)
        return living

    def if_was_assigned(self, full_name, room_type):
        for room_x in self.room_allocations[room_type].keys():
            if full_name in self.room_allocations[room_type][room_x]:
                return(room_x)

    def allocate(self, first_name, last_name, room_name):
        full_name = (first_name + " " + last_name).upper()
        room_name = room_name.upper()

        if full_name not in self.living_space_waiting_list and self.office_waiting_list:
            print(full_name + " - Not in waiting list")

        elif room_name not in self.all_rooms:
            print("Incorrect room name - " + room_name)

        elif full_name in self.all_staff and room_name in self.all_living:
            print("Staff don't get living")

        elif full_name in self.office_waiting_list and room_name in self.all_offices:
            if len(self.room_allocations["office"][room_name]) < 6:
                self.room_allocations["office"][room_name].append(room_name)
            print("office full")

        elif full_name in self.living_space_waiting_list and room_name in self.all_living:
            if len(self.room_allocations["living"][room_name]) < 4:
                self.room_allocations["living"][room_name].append(full_name)
            print("living full")

    def reallocate_person(self, first_name, last_name, room_name):
        full_name = (first_name + " " + last_name).upper()
        room_name = room_name.upper()

        # check if person exists
        if full_name in self.all_people:

            # check if room exists and room is a living space
            if room_name in self.all_rooms and room_name in self.all_living:

                # re allocating living space
                previous_room = self.if_was_assigned(full_name, "living")

                # check if person had living space before reallocation
                if previous_room is None:
                    print("No room assigned, can't be re-assigned")

                # check if reallocation is to current living space
                elif previous_room is room_name:
                    print("Can't reallocate to same room")
                else:
                    # checking availability of new living space and reallocate
                    if len(self.room_allocations["living"][room_name]) < 4:
                        # remove person from old living space
                        self.room_allocations["living"][previous_room].remove(
                            full_name)
                        # add person to new living space
                        self.room_allocations["living"][room_name].append(
                            full_name)

                        print("Reallocated " + full_name + " from " + previous_room +
                              " to " + room_name)
                    # if living space is full
                    else:
                        print("Reallocation failed! %s living space full"
                              % room_name)

            # check if room exists and is an office
            elif room_name in self.all_rooms and room_name in self.all_offices:

                # re allocating office
                previous_room = self.if_was_assigned(full_name, "office")

                # check if person had office before reallocation
                if previous_room is None:
                    print("No office assigned, can't be re-assigned")

                # check if reallocation is to current office
                elif previous_room is room_name:
                    print("Can't reallocate to current room")
                else:
                    # check availability of new office and reallocate
                    if len(self.room_allocations["office"][room_name]) < 6:
                        # remove person from old office
                        self.room_allocations["office"][previous_room].remove(
                            full_name)
                        # add person to new office
                        self.room_allocations["office"][room_name].append(
                            full_name)

                        print("Reallocated " + full_name + " from " + previous_room +
                              " to " + room_name)
                    # if office is full
                    else:
                        print("Reallocation failed! %s office full"
                              % room_name)
            else:
                print("Room name - "+room_name+" doesn't exist!")
        else:
            print("Employee name - " +full_name + " doesn't exist")

    def load_people(self, file_name):
        # add people from txt
        text_file = open(file_name)
        for line in text_file:
            # strip input from file of spaces and new line
            reg = (line.rstrip('\n')).split(" ")
            # check if inputs format is correct
            if len(reg) == 4 and reg[2] in (
             "FELLOW", "STAFF") and reg[3] in ("Y", "N"):

                # adding people if line has 4 values
                self.add_person(reg[0], reg[1], reg[2], reg[3])
            elif len(reg) == 3 and reg[2] in ("FELLOW", "STAFF"):

                # adding people if line has 3 values
                self.add_person(reg[0], reg[1], reg[2])
            else:
                # if data doesn't match format
                return("Incorrect data format")

    def print_people(self):
        print("\nTotal number of people: " + str(len(self.all_people)))
        print("No. of staff is: " + str(len(self.all_staff)))
        print("No. of fellow is: " + str(len(self.all_fellow)))
        for name in self.all_staff:
            print("\nStaff")
            print(name + " - Staff")
        for name in self.all_fellow:
            print("\nFellows")
            print(name + " - Fellow")

    def print_unallocated(self, file_name=None):
        office_waiting = len(self.office_waiting_list)
        living_space_waiting = len(self.living_space_waiting_list)

        empl_msg = "\nEmployees waiting for office: %s \n" % office_waiting
        print(empl_msg)
        # return empl_msg
        for employee in self.office_waiting_list:
            print(employee)
            # return employee

        fell_msg = "\nFellow waiting living space: %s\n" % living_space_waiting
        print(fell_msg)
        # return fell_msg
        for fellow in self.living_space_waiting_list:
            print(fellow)
            # return fellow

        if file_name is not None:
            # temp = file_name.split(".")
            # if len(temp) == 1:
            print("\n Printing out to file - ", file_name)
            # return("\n Printing out to file - ", file_name)
            with open(file_name, 'a') as f:

                # write out all employees without office
                time_stamp = time.strftime("%Y-%m-%d %H:%M")
                f.write("\nUnallocated as of " + time_stamp)
                f.write(empl_msg)
                for employee in self.office_waiting_list:
                    f.write((employee) + "\n")

                # write out fellows without living space
                f.write(fell_msg)
                for fellow in self.living_space_waiting_list:
                    f.write((fellow) + "\n")
            # else:
                # print("Please indicate a valid file name and extension")
                # return("Please indicate a valid file name and extension")

    def print_data(self, room_name):
        room_name = room_name.upper()
        global room_type

        if room_name not in self.all_rooms:
            msg = ("Sorry! Room is none existent")
        else:
            # check if room exists and is an office
            if room_name in self.all_offices:
                room_type = "office"
            elif room_name in self.all_living:
                room_type = "living"

            # print out room name and type
            room_details = (room_name + " - " + room_type)
            h_line = ('-' * 30)
            # print out occupants
            occupants = (',    '.join(self.room_allocations[room_type][room_name]))
            if len(self.room_allocations[room_type][room_name]) == 0:
                occupants = "No occupants"
            msg = (h_line + "\n" + room_details + "\n" + h_line + "\n" + occupants + "\n\n")
        return(msg)

    def print_room(self, room_name):
        print(self.print_data(room_name))

    def print_allocations(self, file_name=None):
        if len(self.all_rooms) < 1:
            print("No rooms available")
        for room in self.all_rooms:
            allocations = self.print_data(room)
            print(allocations)

        if file_name:
            with open(file_name, 'a') as f:
                time_stamp = time.strftime("%Y-%m-%d %H:%M")
                f.write("\nAllocations as of " + time_stamp + "\n")
                for room in self.all_rooms:
                    allocations = self.print_data(room)
                    f.write(allocations)
                f.write("\n\n\n")

    def save_state(self, database="default"):
        # initializing db
        db = database + ".sqlite"
        if os.path.isfile(db) is True:
            os.remove(db)

        print("initializing database")
        db = DatabaseCreator(database)
        Base.metadata.bind = db.engine
        db_session = db.session

        # saving people
        people_in_db = select([Employees])
        result = db_session.execute(people_in_db)
        people_list = [item.emp_name for item in result]

        print("Saving fellows")
        for full_name in self.all_fellow:
            if full_name not in people_list:
                new_person = Employees(emp_name=full_name,
                                       emp_role="Fellow")
                db.session.add(new_person)
                db.session.commit()

        for full_name in self.all_staff:
            if full_name not in people_list:
                new_person = Employees(emp_name=full_name,
                                       emp_role="Staff")
                db.session.add(new_person)
                db.session.commit()

        # saving rooms
        rooms_in_db = select([Rooms])
        result = db_session.execute(rooms_in_db)
        rooms_list = [item.room_name for item in result]

        print("Saving rooms")
        for room_name in self.all_offices:
            if room_name not in rooms_list:
                new_room = Rooms(room_name=room_name,
                                 room_type="Office")
                db.session.add(new_room)
                db.session.commit()

        for room_name in self.all_living:
            if room_name not in rooms_list:
                new_room = Rooms(room_name=room_name,
                                 room_type="Living")
                db.session.add(new_room)
                db.session.commit()

        # saving room allocations
        # unallocated
        print("Saving office allocations")
        allocations_in_db = select([Allocations])
        result = db_session.execute(allocations_in_db)
        allocations_list = [item.room_name for item in result]

        offices = []
        living_spaces = []
        for x in self.all_living:
            living_spaces.append(x)
        for x in self.all_offices:
            offices.append(x)
        for office in offices:
            occupants = ", ".join(self.room_allocations["office"][office])
            if office not in allocations_list:
                allocations = Allocations(room_name=office,
                                          room_type="office",
                                          occupants=occupants)
                db.session.add(allocations)
                db.session.commit()

        for living in living_spaces:
            occupants = ", ".join(self.room_allocations["living"][living])
            if living not in allocations_list:
                allocations = Allocations(room_name=living,
                                          room_type="living",
                                          occupants=occupants)
                db.session.add(allocations)
                db.session.commit()

        print("Saving waiting lists")
        waiting_in_db = select([Unallocated])
        result = db_session.execute(waiting_in_db)
        waiting_list = [item.room_type for item in result]
        unallocated_office = ", ".join(self.office_waiting_list)
        if unallocated_office not in waiting_list:
            unallocated = Unallocated(room_type="office",
                                      unallocated=unallocated_office)
            db.session.add(unallocated)
            db.session.commit()

        unallocated_living = ", ".join(self.living_space_waiting_list)
        if unallocated_living not in waiting_list:
            unallocated = Unallocated(room_type="living",
                                      unallocated=unallocated_living)
            db.session.add(unallocated)
            db.session.commit()

    def load_state(self, database="default"):
        print("initializing database")
        db = DatabaseCreator(database)
        Base.metadata.bind = db.engine
        db_session = db.session

        print("Loading data...")
        print("Loading Employees")
        people_in_db = select([Employees])
        result = db_session.execute(people_in_db)
        for person in result.fetchall():
            self.all_people.append(person.emp_name)
            if person.emp_role.upper() == "FELLOW":
                self.all_fellow.append(person.emp_name)
            elif person.emp_role.upper() == "STAFF":
                self.all_staff.append(person.emp_name)

        print("Loading Rooms")
        rooms_in_db = select([Rooms])
        result = db_session.execute(rooms_in_db)
        for room in result.fetchall():
            self.all_rooms.append(room.room_name)
            if room.room_type.upper() == "OFFICE":
                self.all_offices.append(room.room_name)
                self.room_allocations["office"][room.room_name] = []
            elif room.room_type.upper() == "LIVING":
                self.all_living.append(room.room_name)
                self.room_allocations["living"][room.room_name] = []

        print("Loading Allocations")
        allocations_in_db = select([Allocations])
        result = db_session.execute(allocations_in_db)
        for allocations in result.fetchall():
            occupants = [x.strip() for x in allocations.occupants.split(',')]
            for x in occupants:
                self.room_allocations[allocations.room_type][allocations.room_name].append(x)

        unallocated_in_db = select([Unallocated])
        result = db_session.execute(unallocated_in_db)
        for unallocated in result.fetchall():
            if unallocated[0].upper() == "OFFICE":
                pple = [x.strip() for x in unallocated[1].split(',')]
                for x in pple:
                    if x not in self.office_waiting_list:
                        self.office_waiting_list.append(x)
            if unallocated[0].upper() == "LIVING":
                pple = [x.strip() for x in unallocated[1].split(',')]
                for x in pple:
                    if x not in self.living_space_waiting_list:
                        self.living_space_waiting_list.append(x)

        print("Loading from " + database + " completed successfully")
