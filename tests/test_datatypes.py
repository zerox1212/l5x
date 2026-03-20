"""
Unit tests for controller datatypes and datatype members.
"""

from tests import fixture
import unittest


class DataTypes(unittest.TestCase):
    """Tests for controller datatype access."""
    def setUp(self):
        prj = fixture.string_to_project(r"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<RSLogix5000Content SchemaRevision="1.0" SoftwareRevision="20.01" TargetName="test" TargetType="Controller" ContainsContext="false" Owner="admin" ExportDate="Mon Jul 20 01:45:55 2020" ExportOptions="DecoratedData ForceProtectedEncoding AllProjDocTrans">
<Controller Use="Target" Name="test" ProcessorType="1756-L61" MajorRev="20" MinorRev="11" TimeSlice="20" ShareUnusedTimeSlice="1" ProjectCreationDate="Sat Jul 18 23:53:16 2020" LastModifiedDate="Sat Jul 18 23:53:18 2020" SFCExecutionControl="CurrentActive" SFCRestartPosition="MostRecent"
 SFCLastScan="DontScan" ProjectSN="16#0000_0000" MatchProjectToController="false" CanUseRPIFromProducer="false" InhibitAutomaticFirmwareUpdate="0">
<DataTypes>
<DataType Name="testUDT" Family="NoFamily" Class="User">
<Members>
<Member Name="backing" DataType="SINT" Dimension="0" Radix="Decimal" Hidden="true" ExternalAccess="Read/Write"/>
<Member Name="switch" DataType="BIT" Dimension="0" Radix="Decimal" Hidden="false" Target="backing" BitNumber="0" ExternalAccess="Read/Write"/>
</Members>
</DataType>
<DataType Name="testUDT2" Family="NoFamily" Class="User">
<Members>
<Member Name="struct1" DataType="testUDT" Dimension="0" Radix="NullType" Hidden="false" ExternalAccess="Read/Write"/>
</Members>
</DataType>
</DataTypes>
<Tags/>
<Programs/>
<Modules/>
</Controller>
</RSLogix5000Content>""")
        self.datatypes = prj.controller.datatypes

    def test_names_read(self):
        """Test name attribute returns all datatype names."""
        self.assertEqual(set(self.datatypes.names),
                         set(('testUDT', 'testUDT2')))

    def test_names_read_only(self):
        """Ensure names attribute is read-only."""
        with self.assertRaises(AttributeError):
            self.datatypes.names = 'foo'

    def test_index(self):
        """Test indexing by names."""
        for datatype in self.datatypes.names:
            self.datatypes[datatype]

    def test_member_names(self):
        """Ensure members names attribute is iterable."""
        self.assertEqual(set(self.datatypes['testUDT'].members.names),
                         set(('backing', 'switch')))

    def test_member_attributes(self):
        """Confirm member attributes are exposed."""
        member = self.datatypes['testUDT'].members['switch']
        self.assertEqual(member.data_type, 'BIT')
        self.assertEqual(member.dimension, '0')
        self.assertEqual(member.radix, 'Decimal')
        self.assertEqual(member.target, 'backing')
        self.assertEqual(member.bit_number, '0')
        self.assertEqual(member.external_access, 'Read/Write')
        self.assertFalse(member.hidden)

    def test_datatype_attributes(self):
        """Confirm datatype attributes are exposed."""
        datatype = self.datatypes['testUDT']
        self.assertEqual(datatype.family, 'NoFamily')
        self.assertEqual(datatype.class_name, 'User')
