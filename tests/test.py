
"""test/tests"""
import os
import unittest
import unittest.mock as mock
from amity.app import amity


class TestCase(unittest.TestCase):
    def setUp(self):

        self.amity = amity.Amity()

    def test_create_office(self):
        rooms_count_before = len(self.amity.all_rooms)
        offices_count_before = len(self.amity.all_offices)

        # test message after adding Office
        self.assertEqual(self.amity.create_room(
            "Oculus", "Office"), "Office Added")

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
            "Golang", "living"), "Living space Added")

        rooms_count_after = len(self.amity.all_rooms)
        living_count_after = len(self.amity.all_living)

        # check if living and office count increased by 1
        self.assertEqual(rooms_count_before + 1, rooms_count_after)
        self.assertEqual(offices_count_before + 1, offices_count_after)

        # check that room has been added
        self.assertTrue("GOLANG" in self.amity.all_rooms)
        self.assertTrue("GOLANG" in self.amity.all_living)

        # test if rooms is added to dict with list
        self.assertDictContainsSubset(
            self.amity.room_allocations["living"], {"GOLANG": []})

    def test_create_wrong_room_type(self):
        rooms_count_before = len(self.amity.all_rooms)

        # test for wrong room_type
        self.assertEqual(self.amity.create_room(
            "Yellow", "Home"), "Wrong Room Type")
        rooms_count_after = len(self.amity.all_rooms)

        # check if rooms before is equal to current number of rooms
        self.assertEqual(rooms_count_before, rooms_count_after)

        # check room not added
        self.assertFalse('YELLOW' in self.amity.all_rooms)

    def test_create_room_that_exists(self):
        rooms_count_before = len(self.amity.all_rooms)

        # test message after re adding room
        self.assertEqual(self.amity.create_room(
            "Golang", "living"), "GOLANG room name already used")

        rooms_count_after = len(self.amity.all_rooms)
        # check if rooms before is equal to current number of rooms
        self.assertEqual(rooms_count_before, rooms_count_after)

        # check that room is actually there
        self.assertTrue('GOLANG' in self.amity.all_rooms)

    def test_add_staff(self):
        people_count_before = len(self.amity.all_people)
        staff_count_before = len(self.amity.all_staff)

        # return message for successfully adding staff
        self.assertEqual(
            self.amity.add_person("Per", "Njira", "Staff"),
            "PER NJIRA - staff added successfully")

        people_count_after = len(self.amity.all_people)
        staff_count_after = len(self.amity.all_staff)

        # check if staff and people count has increased by 1
        self.assertEqual(people_count_before + 1, people_count_after)
        self.assertEqual(staff_count_before + 1, staff_count_after)

    def test_add_fellow(self):
        people_count_before = len(self.amity.all_people)
        fellow_count_before = len(self.amity.all_fellow)

        # return message for successfully adding fellow
        self.assertEqual(
            self.amity.add_person("Joe", "Musau", "Fellow", "Y"),
            "JOE MUSAU - fellow added successfully")

        people_count_after = len(self.amity.all_people)
        fellow_count_after = len(self.amity.all_fellow)

        # check if fellow and people count has increased by 1
        self.assertEqual(people_count_before + 1, people_count_after)
        self.assertEqual(fellow_count_before + 1, fellow_count_after)

    def test_add_person_existing(self):
        people_count_before = len(self.amity.all_people)

        # test adding a name already used
        self.assertEqual(self.amity.add_person(
            "Joe", "Musau", "Fellow", "Y"), "JOE MUSAU already used")

        people_count_after = len(self.amity.all_people)

        # check if previous count is same as current
        self.assertEqual(people_count_before, people_count_after)

    def test_add_wrong_role(self):
        people_count_before = len(self.amity.all_people)

        # test wrong role input
        self.assertEqual(self.amity.add_person(
            "James", "Muli", "Trainer", "Y"), "Please indicate correct role")

        people_count_after = len(self.amity.all_people)

        # check if previous count is same as current
        self.assertEqual(people_count_before, people_count_after)

    def test_reallocate_person(self):
        first_room_occupants = len(self.amity.room_allocations[
            "living"]["JAVA"])

        # person created and  allocated random room e.g JAVA
        self.amity.add_person("Jose", "Kit", "Fellow", "Y")

        # create new room for reallocation
        self.amity.create_room("PHP", "LIVING")

        second_room_occupants = len(self.amity.room_allocations["living"]["PHP"])

        # re allocation
        self.amity.reallocate_person("JOSE", "KIT", "PHP")
        first_room_new_occupants = len(self.amity.room_allocations["living"]["JAVA"])
        second_room_new_occupants = len(self.amity.room_allocations["living"]["PHP"])

        # check if old room occupants reduce
        self.assertEqual(first_room_occupants - 1, first_room_new_occupants)
        # check if new room occupants increased
        self.assertEqual(second_room_occupants + 1, second_room_new_occupants)

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


# if __name__ == '__main__':
#     unittest.main()
