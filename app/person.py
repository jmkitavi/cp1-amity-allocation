"""app/person"""


class Person(object):
    """Person."""
    def __init__(self, first_name, last_name, role, accomodation='N'):
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.accomodation = accomodation


class Fellow(Person):
    def __init__(self, first_name, last_name, role, accomodation="N"):
        super(Fellow, self).__init__(first_name, last_name, role, accomodation)


class Staff(Person):
    def __init__(self, first_name, last_name, role, accomodation="N"):
        super(Fellow, self).__init__(first_name, last_name, role, accomodation)
