
"""test/tests"""
import os
import unittest
import unittest.mock as mock
from app import amity
from termcolor import colored


class TestCase(unittest.TestCase):
    def setUp(self):
        """ Setting up attributes for class Amity. """
        self.amity = amity.Amity()

    def test_create_office(self):
        """ Test for creating office. Office should be added. """
        rooms_count_before = len(self.amity.all_rooms)
        offices_count_before = len(self.amity.all_offices)

        # test message after adding Office
        self.assertEqual(self.amity.create_room(
            "office", "Oculus"), "OCULUS - office added successfully")

        offices_count_after = len(self.amity.all_offices)
        rooms_count_after = len(self.amity.all_rooms)

        # check if room and office count has increased by 1
        self.assertEqual(rooms_count_before + 1, rooms_count_after)
        self.assertEqual(offices_count_before + 1, offices_count_after)

        # check that room has been added
        self.assertTrue("OCULUS" in self.amity.all_rooms)
        self.assertTrue("OCULUS" in self.amity.all_offices)

        # test if rooms is added to dict with list
        self.assertDictContainsSubset(
            self.amity.room_allocations["office"], {"OCULUS": []})

    def test_create_living(self):
        """ Test for creating living. Living should be added. """
        rooms_count_before = len(self.amity.all_rooms)
        living_count_before = len(self.amity.all_living)

        # test return message after adding living space
        self.assertEqual(self.amity.create_room(
            "living", "go"), "GO - living space added successfully")

        rooms_count_after = len(self.amity.all_rooms)
        living_count_after = len(self.amity.all_living)

        # check if living and office count increased by 1
        self.assertEqual(rooms_count_before + 1, rooms_count_after)
        self.assertEqual(living_count_before + 1, living_count_after)

        # check that room has been added
        self.assertTrue("GO" in self.amity.all_rooms)
        self.assertTrue("GO" in self.amity.all_living)

        # test if rooms is added to dict with list
        self.assertDictContainsSubset(
            self.amity.room_allocations["living"], {"GO": []})

    def test_create_wrong_room_type(self):
        """ Test for wrong room types. Room should not be added. """
        rooms_count_before = len(self.amity.all_rooms)

        # test for wrong room_type
        self.assertEqual(self.amity.create_room(
            "home", "YELLOW"), (colored("HOME is a wrong room type - Office or Living", "red")))
        rooms_count_after = len(self.amity.all_rooms)

        # check if rooms before is equal to current number of rooms
        self.assertEqual(rooms_count_before, rooms_count_after)

        # check room not added
        self.assertFalse('YELLOW' in self.amity.all_rooms)

    def test_create_room_that_exists(self):
        """ Test creating room that exists. Room should not be added. """
        self.amity.create_room("living", "go")

        rooms_count_before = len(self.amity.all_rooms)
        # test message after re adding room
        self.assertEqual(self.amity.create_room(
            "living", "GO"), colored("Sorry! GO - room name already used", "red"))

        rooms_count_after = len(self.amity.all_rooms)
        # check if rooms before is equal to current number of rooms
        self.assertEqual(rooms_count_before, rooms_count_after)

        # check that room is actually there
        self.assertTrue('GO' in self.amity.all_rooms)

    def test_add_staff(self):
        """ Test adding staff. Staff and Employees number should increase. """
        people_count_before = len(self.amity.all_people)
        staff_count_before = len(self.amity.all_staff)

        self.amity.add_person("Per", "Njira", "Staff")

        people_count_after = len(self.amity.all_people)
        staff_count_after = len(self.amity.all_staff)

        # check if staff and people count has increased by 1
        self.assertEqual(people_count_before + 1, people_count_after)
        self.assertEqual(staff_count_before + 1, staff_count_after)

    def test_add_fellow(self):
        """ Test adding fellow. Staff and Fellow number should increase. """
        people_count_before = len(self.amity.all_people)
        fellow_count_before = len(self.amity.all_fellow)

        self.amity.add_person("Joe", "Musau", "Fellow", "Y")

        people_count_after = len(self.amity.all_people)
        fellow_count_after = len(self.amity.all_fellow)

        # check if fellow and people count has increased by 1
        self.assertEqual(people_count_before + 1, people_count_after)
        self.assertEqual(fellow_count_before + 1, fellow_count_after)

    def test_add_person_existing(self):
        """ Test add existing person. People should not increase. """
        self.amity.add_person("Joe", "Musau", "Fellow", "Y")
        people_count_before = len(self.amity.all_people)

        # test adding a name already used
        self.assertEqual(self.amity.add_person(
            "Joe", "Musau", "Fellow", "Y"), colored("Sorry! Name JOE MUSAU already used", "red"))

        people_count_after = len(self.amity.all_people)

        # check if previous count is same as current
        self.assertEqual(people_count_before, people_count_after)

    def test_add_wrong_role(self):
        """ Test add person with wrong role. Person should not be added. """
        people_count_before = len(self.amity.all_people)

        # test wrong role input
        self.assertEqual(self.amity.add_person(
            "James", "Muli", "Trainer", "Y"), colored("Error! Please indicate correct role.\n\t Fellow or Staff", "red"))

        people_count_after = len(self.amity.all_people)

        # check if previous count is same as current
        self.assertEqual(people_count_before, people_count_after)

    def test_reallocate_person_living(self):
        """" Test re-allocating person to living. Check if living changes. """
        # person created and  allocated random room e.g JAVA
        self.amity.create_room("living", "java")
        self.amity.add_person("Jose", "Kit", "Fellow", "Y")
        first_room_occupants = len(self.amity.room_allocations[
            "living"]["JAVA"])

        # create new room for reallocation
        self.amity.create_room("living", "php")
        second_room_occupants = len(self.amity.room_allocations["living"]["PHP"])

        # re allocation
        self.amity.reallocate_person("JOSE", "KIT", "PHP")
        first_room_new_occupants = len(self.amity.room_allocations["living"]["JAVA"])
        second_room_new_occupants = len(self.amity.room_allocations["living"]["PHP"])

        # check if old room occupants reduce
        self.assertEqual(first_room_occupants - 1, first_room_new_occupants)
        # check if new room occupants increased
        self.assertEqual(second_room_occupants + 1, second_room_new_occupants)

    def test_reallocate_person_office(self):
        """" Test re-allocating person to office. Check if office changes. """

        # person created and  allocated random room e.g JAVA
        self.amity.create_room("office", "ocu")
        self.amity.add_person("Jose", "Kit", "fellow")
        first_room_occupants = len(self.amity.room_allocations[
            "office"]["OCU"])

        # create new room for reallocation
        self.amity.create_room("office", "hog")
        second_room_occupants = len(self.amity.room_allocations["office"]["HOG"])

        # re allocation
        self.amity.reallocate_person("JOSE", "KIT", "HOG")
        first_room_new_occupants = len(self.amity.room_allocations["office"]["OCU"])
        second_room_new_occupants = len(self.amity.room_allocations["office"]["HOG"])

        # check if old room occupants reduce
        self.assertEqual(first_room_occupants - 1, first_room_new_occupants)
        # check if new room occupants increased
        self.assertEqual(second_room_occupants + 1, second_room_new_occupants)

    def reallocate_none_room(self):
        """ Test reallocating to room that isn't created. Return error. """
        self.amity.create_room("office", "Hog")
        self.amity.add_person("John", "Doe", "Fellow")
        self.assertEqual(self.reallocate("John", "Doe", "Ocu"), "Room name - OCU doesn't exist!")

    def test_select_random_office(self):
        """ Test random office selection. """
        # select random with no office
        self.assertEqual(self.amity.select_random_office(), False)
        # create one office
        self.amity.create_room("office", "Oculus")
        # select random with one office created
        self.assertEqual(self.amity.select_random_office(), "OCULUS")

    def test_select_random_living(self):
        """ Test random living selection. """
        # select random with no living
        self.assertEqual(self.amity.select_random_living(), False)
        # create one living
        self.amity.create_room("living", "java")
        # select random with one living created
        self.assertEqual(self.amity.select_random_living(), "JAVA")

    def test_if_was_assigned(self):
        """ Test checking if someone was assigned room before. """
        # create office
        self.amity.create_room("office", "java")
        # add new person, assigned randomly to java
        self.amity.add_person("Joe", "Kit", "Fellow")
        # check if assigned
        self.assertEqual(self.amity.if_was_assigned("JOE KIT", "office"), "JAVA")

    def test_allocate(self):
        """ Test allocating rooms to people in waiting list. """
        # create person, unallocated
        self.amity.add_person("Joe", "Kit", "Fellow")
        unallocated_before = len(self.amity.office_waiting_list)
        # create office to allocate person to
        self.amity.create_room("office", "oculus")
        occupants_before = len(self.amity.room_allocations["office"]["OCULUS"])
        # allocate to office
        self.assertEqual(self.amity.allocate("Joe", "Kit", "oculus"), "JOE KIT successfully assigned office - OCULUS")

        unallocated_after = len(self.amity.office_waiting_list)
        occupants_after = len(self.amity.room_allocations["office"]["OCULUS"])

        # unallocated reduces
        self.assertEqual(unallocated_before - 1, unallocated_after)
        # occupants increase
        self.assertEqual(occupants_before + 1, occupants_after)

    def test_allocate_non_person(self):
        """ Test allocating someone who doesn't exist. Return error. """
        self.assertEqual(self.amity.allocate("Je", "Me", "go"), "JE ME - name doesn't exist")

    def test_allocate_no_room(self):
        """ Test allocating room which doesn't exist. Return error. """
        self.amity.add_person("Je", "Me", "Fellow")
        self.assertEqual(self.amity.allocate("Je", "Me", "go"), "Incorrect room name - GO")

    def test_load_people(self):
        """ Test loading people from a text file. """
        # load data
        self.amity.load_people("load.txt")
        # check if file exists
        self.assertTrue(os.path.isfile("load.txt"))
        # check if all people were added
        self.assertEqual(len(self.amity.all_people), 6)
        # check if staff has been added
        self.assertEqual(len(self.amity.all_staff), 2)
        # check if fellow in file were added
        self.assertEqual(len(self.amity.all_fellow), 4)

    def test_print_unallocated(self):
        """ Test creation of file when print unallocated to file. """
        # test for file creation for output
        self.amity.print_unallocated("new")
        self.assertTrue(os.path.isfile("new"))

    def test_print_data(self):
        """ Test print data about a room. """
        self.assertEqual(self.amity.print_data("java"), "Sorry! Room is none existent")

    def test_print_allocation(self):
        """" Test print allocations with no rooms. """
        self.assertEqual(self.amity.print_allocations(), "No rooms available")

    def test_print_allocation_file(self):
        """ Test print allocations to a file. """
        self.amity.create_room("office", "hog")
        self.amity.print_allocations("out")
        self.assertTrue(os.path.isfile("out"))

    def test_save_state(self):
        """ Test save amity state to Database. """
        self.amity.add_person("Joe", "Kit", "fellow")
        self.amity.save_state("test")
        self.assertTrue(os.path.isfile("test.sqlite"))

    def test_load_state(self):
        """ Test loading amity state from Database. """
        people_count_before = len(self.amity.all_people)
        self.amity.load_state("test")
        people_count_after = len(self.amity.all_people)
        self.assertEqual(people_count_before + 1, people_count_after)

    def test_load_state_no_database(self):
        """" Test load state when there's no Database. """
        self.assertEqual(self.amity.load_state("none"), "Database none.sqlite not found")

    def tearDown(self):
        pass
