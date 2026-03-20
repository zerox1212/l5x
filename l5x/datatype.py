"""
Objects implementing datatype access.
"""

from .dom import (ElementDict, AttributeDescriptor)


class BooleanAttribute(AttributeDescriptor):
    """Descriptor class for boolean XML attributes."""
    def from_xml(self, raw):
        return True if raw == 'true' else False


class DataType(object):
    """Accessor object for a single data type."""
    family = AttributeDescriptor('Family', True)
    class_name = AttributeDescriptor('Class', True)

    def __init__(self, element, lang=None):
        self.element = element
        self.lang = lang
        members = element.find('Members')
        self.members = ElementDict(members, 'Name', Member)


class Member(object):
    """Accessor object for a single datatype member."""
    data_type = AttributeDescriptor('DataType', True)
    dimension = AttributeDescriptor('Dimension', True)
    radix = AttributeDescriptor('Radix', True)
    hidden = BooleanAttribute('Hidden', True)
    target = AttributeDescriptor('Target', True)
    bit_number = AttributeDescriptor('BitNumber', True)
    external_access = AttributeDescriptor('ExternalAccess', True)

    def __init__(self, element):
        self.element = element
