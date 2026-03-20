"""
Unit tests for a program's routines object.
"""

from tests import fixture
import l5x
import unittest
from l5x import dom


class Routines(unittest.TestCase):
    """Tests for routines collected under a program object."""
    def setUp(self):
        prj = fixture.string_to_project(r"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<RSLogix5000Content SchemaRevision="1.0" SoftwareRevision="20.01" TargetName="test" TargetType="Controller" ContainsContext="false" Owner="admin" ExportDate="Mon Jul 20 01:45:55 2020" ExportOptions="DecoratedData ForceProtectedEncoding AllProjDocTrans">
<Controller Use="Target" Name="test" ProcessorType="1756-L61" MajorRev="20" MinorRev="11" TimeSlice="20" ShareUnusedTimeSlice="1" ProjectCreationDate="Sat Jul 18 23:53:16 2020" LastModifiedDate="Sat Jul 18 23:53:18 2020" SFCExecutionControl="CurrentActive" SFCRestartPosition="MostRecent"
 SFCLastScan="DontScan" ProjectSN="16#0000_0000" MatchProjectToController="false" CanUseRPIFromProducer="false" InhibitAutomaticFirmwareUpdate="0">
<Programs>
<Program Name="MainProgram" TestEdits="false" Disabled="false">
<Tags/>
<Routines>
<Routine Name="MainRoutine" Type="RLL">
<RLLContent>
<Rung Number="0" Type="N">
<Comment>
<![CDATA[test description]]>
</Comment>
<Text>
<![CDATA[XIC(testTag)NOP();]]>
</Text>
</Rung>
<Rung Number="1" Type="N">
<Text>
<![CDATA[NOP();]]>
</Text>
</Rung>
</RLLContent>
</Routine>
<Routine Name="AnotherRoutine" Type="ST"/>
</Routines>
</Program>
</Programs>
</Controller>
</RSLogix5000Content>""")
        self.program = prj.programs['MainProgram']

    def test_routines_wrapper_type(self):
        """Confirm routines is exposed as a wrapper class."""
        self.assertIsInstance(self.program.routines, l5x.project.Routines)

    def test_names_read(self):
        """Test names attribute returns all routine names."""
        self.assertEqual(set(self.program.routines.names),
                         set(('MainRoutine', 'AnotherRoutine')))

    def test_names_read_only(self):
        """Ensure names attribute is read-only."""
        with self.assertRaises(AttributeError):
            self.program.routines.names = 'foo'

    def test_index(self):
        """Test indexing by name."""
        for routine in self.program.routines.names:
            self.program.routines[routine]

    def test_invalid_index(self):
        """Verify accessing a nonexistent routine raises an exception."""
        with self.assertRaises(KeyError):
            self.program.routines['not_a_routine']

    def test_type_read(self):
        """Confirm the routine type is exposed."""
        self.assertEqual(self.program.routines['MainRoutine'].type, 'RLL')

    def test_type_read_only(self):
        """Confirm an exception is raised when changing the routine type."""
        with self.assertRaises(AttributeError):
            self.program.routines['MainRoutine'].type = 'ST'

    def test_rungs_wrapper_type(self):
        """Confirm ladder routines expose a rungs wrapper."""
        self.assertIsInstance(self.program.routines['MainRoutine'].rungs,
                              l5x.project.Rungs)

    def test_rung_numbers(self):
        """Confirm rungs are indexed by rung number."""
        self.assertEqual(self.program.routines['MainRoutine'].rungs.names,
                         [0, 1])
        self.program.routines['MainRoutine'].rungs[0]
        self.program.routines['MainRoutine'].rungs[1]

    def test_rung_number_read_only(self):
        """Confirm an exception is raised when changing the rung number."""
        with self.assertRaises(AttributeError):
            self.program.routines['MainRoutine'].rungs[0].number = 1

    def test_rung_comment_read(self):
        """Confirm reading an existing rung comment."""
        rung = self.program.routines['MainRoutine'].rungs[0]
        self.assertEqual(rung.comment, 'test description')

    def test_rung_comment_write(self):
        """Confirm updating a rung comment preserves CDATA content."""
        rung = self.program.routines['MainRoutine'].rungs[0]
        rung.comment = 'updated description'
        self.assert_cdata_child(rung.element.find('Comment'),
                                'updated description')

    def test_rung_comment_create(self):
        """Confirm creating a new rung comment inserts a Comment element."""
        rung = self.program.routines['MainRoutine'].rungs[1]
        rung.comment = 'new comment'
        children = [child.tag for child in rung.element]
        self.assertEqual(children, ['Comment', 'Text'])
        self.assert_cdata_child(rung.element.find('Comment'), 'new comment')

    def test_rung_comment_delete(self):
        """Confirm removing a rung comment deletes the Comment element."""
        rung = self.program.routines['MainRoutine'].rungs[0]
        rung.comment = None
        self.assertIsNone(rung.element.find('Comment'))

    def test_rung_text_read(self):
        """Confirm reading an existing rung text."""
        rung = self.program.routines['MainRoutine'].rungs[0]
        self.assertEqual(rung.text, 'XIC(testTag)NOP();')

    def test_rung_text_write(self):
        """Confirm updating rung text preserves CDATA content."""
        rung = self.program.routines['MainRoutine'].rungs[1]
        rung.text = 'XIO(testTag)NOP();'
        self.assert_cdata_child(rung.element.find('Text'), 'XIO(testTag)NOP();')

    def assert_cdata_child(self, element, text):
        """Verifies an element contains a single CDATA child with text."""
        children = list(element)
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].tag, dom.CDATA_TAG)
        self.assertEqual(children[0].text, text)
