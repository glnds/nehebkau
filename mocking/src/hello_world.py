from __future__ import print_function
from model import Person


def lambda_handler(event, context):
    print(Person)
    person = Person()
    print('-----------')
    print(person)
    name = person.get_name()
    print(name)
    return "Hello world"
