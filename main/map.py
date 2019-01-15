from .sql import *

# This file only stores tuples
# These tuples may be used for drop down lists
# or they may be just here to act as a key value pairing

condition = [
    ('New', 'New'),
    ('Used', 'Used'),
    ('Poor', 'Poor'),
]

search_condition = [('Any', 'Any')] + condition

department = [
    ('APSC', 'APSC'),
    ('BIOL', 'BIOL'),
    ('CHEM', 'CHEM'),
    ('CPSC', 'CPSC'),
    ('ENGL', 'EMGL'),
    ('HIST', 'HIST'),
    ('MATH', 'MATH'),
    ('NURS', 'NURS'),
    ('PHIL', 'PHIL'),
    ('PHYS', 'PHYS'),
    ('POLI', 'POLI'),
    ('STAT', 'STAT'),
    ('OTHER', 'OTHER'),
]

search_department = [('Any', 'Any')] + department

price_range = {
    (-1, 'Any'),
    (100, '0-100'),
    (200, '101-200'),
}

terms = [
    (1, 'Spring'),
    (2, 'Summer'),
    (3, 'Winter'),
    (-1, 'Other'),
]

years = [
    (2017, '2017'),
    (2016, '2016'),
    (2015, '2015'),
    (2014, '2014'),
    (2013, '2013'),
]


class Ddl:
    """
    Class to build the dynamic drop down lists
    """

    @staticmethod
    def user_listing():
        return Sql.get_delete_ddl()

    @staticmethod
    def schools():
        return Sql.get_all_school()

    @staticmethod
    def add_listing():
        return Sql.get_add_ddl()
