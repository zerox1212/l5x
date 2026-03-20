"""
Objects implementing logic routine and rung access.
"""

from .dom import (ElementDict, AttributeDescriptor, ElementCDATA)


class CollectionNames(object):
    """Descriptor class to proxy a wrapped ElementDict's names attribute."""
    def __get__(self, instance, owner=None):
        return instance.members.names

    def __set__(self, instance, value):
        raise AttributeError('Read-only attribute.')


class Routines(object):
    """Accessor object for a parent's routines."""
    names = CollectionNames()

    def __init__(self, element, lang):
        self.element = element
        self.members = ElementDict(element, 'Name', Routine, value_args=[lang])

    def __getitem__(self, key):
        return self.members[key]


class Routine(object):
    """Accessor object for a routine."""
    type = AttributeDescriptor('Type', True)

    def __init__(self, element, lang):
        self.element = element
        self.lang = lang
        content = element.find('RLLContent')
        if content is not None:
            self.rungs = Rungs(content, lang)


class Rungs(object):
    """Accessor object for a routine's rungs."""
    names = CollectionNames()

    def __init__(self, element, lang):
        self.element = element
        self.members = ElementDict(element, 'Number', Rung,
                                   key_type=int, value_args=[lang])

    def __getitem__(self, key):
        return self.members[key]


class Rung(object):
    """Accessor object for a rung."""
    number = AttributeDescriptor('Number', True)
    type = AttributeDescriptor('Type', True)
    comment = ElementCDATA('Comment')
    text = ElementCDATA('Text', ['Comment'])

    def __init__(self, element, lang):
        self.element = element
        self.lang = lang
