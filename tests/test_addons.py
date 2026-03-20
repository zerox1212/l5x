"""
Unit tests for controller add-on instruction definitions.
"""

from tests import fixture
import unittest


class AddOns(unittest.TestCase):
    """Tests for controller add-on instruction definition access."""
    def setUp(self):
        prj = fixture.string_to_project(r"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<RSLogix5000Content SchemaRevision="1.0" SoftwareRevision="20.01" TargetName="test" TargetType="Controller" ContainsContext="false" Owner="admin" ExportDate="Mon Jul 20 01:45:55 2020" ExportOptions="DecoratedData ForceProtectedEncoding AllProjDocTrans">
<Controller Use="Target" Name="test" ProcessorType="1756-L61" MajorRev="20" MinorRev="11" TimeSlice="20" ShareUnusedTimeSlice="1" ProjectCreationDate="Sat Jul 18 23:53:16 2020" LastModifiedDate="Sat Jul 18 23:53:18 2020" SFCExecutionControl="CurrentActive" SFCRestartPosition="MostRecent"
 SFCLastScan="DontScan" ProjectSN="16#0000_0000" MatchProjectToController="false" CanUseRPIFromProducer="false" InhibitAutomaticFirmwareUpdate="0">
<DataTypes/>
<Tags/>
<Programs/>
<Modules/>
<AddOnInstructionDefinitions>
<AddOnInstructionDefinition Name="DeviceDO" Revision="1.0" Vendor="KE" ExecutePrescan="false" ExecutePostscan="false" ExecuteEnableInFalse="false" CreatedDate="2023-10-05T18:28:39.092Z" CreatedBy="KNOBELSDORFF\Jeremy.Noble" EditedDate="2026-03-18T20:48:57.767Z" EditedBy="AzureAD\AndrewJenkins" SoftwareRevision="v36.02"/>
<AddOnInstructionDefinition Name="DeviceDI" Revision="1.1" Vendor="KE" ExecutePrescan="true" ExecutePostscan="false" ExecuteEnableInFalse="true" CreatedDate="2023-10-06T18:28:39.092Z" CreatedBy="KNOBELSDORFF\Jeremy.Noble" EditedDate="2026-03-19T20:48:57.767Z" EditedBy="AzureAD\AndrewJenkins" SoftwareRevision="v36.02"/>
</AddOnInstructionDefinitions>
</Controller>
</RSLogix5000Content>""")
        self.addons = prj.controller.addons

    def test_names_read(self):
        """Test name attribute returns all add-on definition names."""
        self.assertEqual(set(self.addons.names), set(('DeviceDO', 'DeviceDI')))

    def test_names_read_only(self):
        """Ensure names attribute is read-only."""
        with self.assertRaises(AttributeError):
            self.addons.names = 'foo'

    def test_index(self):
        """Test indexing by names."""
        for addon in self.addons.names:
            self.addons[addon]

    def test_attributes(self):
        """Confirm add-on definition attributes are exposed."""
        addon = self.addons['DeviceDO']
        self.assertEqual(addon.revision, '1.0')
        self.assertEqual(addon.vendor, 'KE')
        self.assertEqual(addon.execute_prescan, 'false')
        self.assertEqual(addon.execute_postscan, 'false')
        self.assertEqual(addon.execute_enable_in_false, 'false')
        self.assertEqual(addon.created_date, '2023-10-05T18:28:39.092Z')
        self.assertEqual(addon.created_by, r'KNOBELSDORFF\Jeremy.Noble')
        self.assertEqual(addon.edited_date, '2026-03-18T20:48:57.767Z')
        self.assertEqual(addon.edited_by, r'AzureAD\AndrewJenkins')
        self.assertEqual(addon.software_revision, 'v36.02')
