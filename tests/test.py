
"""test/tests"""
import os
import unittest
import unittest.mock as mock
from amity.app import amity
from termcolor import colored


class TestCase(unittest.TestCase):
    def setUp(self):

        self.amity = amity.Amity()

    def test_create_one_office(self):
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
        people_count_before = len(self.amity.all_people)
        staff_count_before = len(self.amity.all_staff)

        self.amity.add_person("Per", "Njira", "Staff")
        # return message for successfully adding staff
        # self.assertEqual(
        #     self.amity.add_person("Per", "Njira", "Staff"),
        #     "PER NJIRA - staff, added successfully\n")

        people_count_after = len(self.amity.all_people)
        staff_count_after = len(self.amity.all_staff)

        # check if staff and people count has increased by 1
        self.assertEqual(people_count_before + 1, people_count_after)
        self.assertEqual(staff_count_before + 1, staff_count_after)

    def test_add_fellow(self):
        people_count_before = len(self.amity.all_people)
        fellow_count_before = len(self.amity.all_fellow)

        self.amity.add_person("Joe", "Musau", "Fellow", "Y")
        # return message for successfully adding fellow
        # self.assertEqual(
        #     self.amity.add_person("Joe", "Musau", "Fellow", "Y"),
        #     "JOE MUSAU - fellow added successfully")

        people_count_after = len(self.amity.all_people)
        fellow_count_after = len(self.amity.all_fellow)

        # check if fellow and people count has increased by 1
        self.assertEqual(people_count_before + 1, people_count_after)
        self.assertEqual(fellow_count_before + 1, fellow_count_after)

    def test_add_person_existing(self):
        self.amity.add_person("Joe", "Musau", "Fellow", "Y")
        people_count_before = len(self.amity.all_people)

        # test adding a name already used
        self.assertEqual(self.amity.add_person(
            "Joe", "Musau", "Fellow", "Y"), colored("Sorry! Name JOE MUSAU already used", "red"))

        people_count_after = len(self.amity.all_people)

        # check if previous count is same as current
        self.assertEqual(people_count_before, people_count_after)

    def test_add_wrong_role(self):
        people_count_before = len(self.amity.all_people)

        # test wrong role input
        self.assertEqual(self.amity.add_person(
            "James", "Muli", "Trainer", "Y"), colored("Error! Please indicate correct role.\n\t Fellow or Staff", "red"))

        people_count_after = len(self.amity.all_people)

        # check if previous count is same as current
        self.assertEqual(people_count_before, people_count_after)

    def test_reallocate_person(self):
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

    def test_select_random_office(self):
        # select random with no office
        self.assertEqual(self.amity.select_random_office(), False)
        # create one office
        self.amity.create_room("office", "Oculus")
        # select random with one office created
        self.assertEqual(self.amity.select_random_office(), "OCULUS")

    def test_select_random_living(self):
        # select random with no living
        self.assertEqual(self.amity.select_random_living(), False)
        # create one living
        self.amity.create_room("living", "java")
        # select random with one living created
        self.assertEqual(self.amity.select_random_living(), "JAVA")

    def test_if_was_assigned(self):
        # create office
        self.amity.create_room("office", "java")
        # add new person, assigned randomly to java
        self.amity.add_person("Joe", "Kit", "Fellow")
        # check if assigned
        self.assertEqual(self.amity.if_was_assigned("JOE KIT", "office"), "JAVA")

    def test_allocate(self):
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



    def test_load_people(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        # load data
        self.amity.load_people(os.path.join(dirname, "load.txt"))
        # check if file exists
        self.assertTrue(os.path.isfile("load.txt"))
        # check if all people were added
        self.assertEqual(len(self.amity.all_people), 2)
        # check if staff has been added
        self.assertEqual(len(self.amity.all_staff), 1)
        # check if fellow in file were added
        self.assertEqual(len(self.amity.all_fellow), 1)

    @mock.patch('app.amity.open')
    def test_print_unallocated(self, mock_open):
        # test for file creation for output
        self.amity.print_unallocated("output")
        mock_open.assert_called_with("output.txt")

    def test_print_room(self):
        self.amity.print_room("JAVA")
        # check if the room is actually there
        self.assertDictContainsSubset(
            self.amity.room_allocations["living"], {"JAVA": []})

    @mock.patch('app.amity.open')
    def test_save_state(self):
        self.amity.save_state("backup")
        # check if database has been created
        mock_open.assert_called_with("backup.sqlite")

    def test_load_state(self):
        self.amity.load_state("data")
        # check if database exists
        self.assertTrue(os.path.isfile("data.sqlite"))
    # def tearDown(self):
    #     pass
#
#
# # if __name__ == '__main__':
# #     unittest.main()
