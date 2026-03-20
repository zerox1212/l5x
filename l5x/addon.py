"""
Objects implementing add-on instruction definition access.
"""

from .dom import AttributeDescriptor


class AddOnInstructionDefinition(object):
    """Accessor object for a single add-on instruction definition."""
    revision = AttributeDescriptor('Revision', True)
    vendor = AttributeDescriptor('Vendor', True)
    execute_prescan = AttributeDescriptor('ExecutePrescan', True)
    execute_postscan = AttributeDescriptor('ExecutePostscan', True)
    execute_enable_in_false = AttributeDescriptor('ExecuteEnableInFalse', True)
    created_date = AttributeDescriptor('CreatedDate', True)
    created_by = AttributeDescriptor('CreatedBy', True)
    edited_date = AttributeDescriptor('EditedDate', True)
    edited_by = AttributeDescriptor('EditedBy', True)
    software_revision = AttributeDescriptor('SoftwareRevision', True)

    def __init__(self, element):
        self.element = element
