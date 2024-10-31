import unittest
from maya import cmds
from maya.api import OpenMaya as om


class TestMaya(unittest.TestCase):
    def test_maya(self):
        self.assertEqual(cmds.about(a=True), "maya")

    def test_maya_state(self):
        self.assertIs(om.MGlobal.mayaState(), om.MGlobal.kLibraryApp)

    def test_node_creation_cmds(self):
        locator = cmds.createNode("locator")
        self.assertTrue(cmds.objExists(locator))

    def test_node_creation_om(self):
        locator = om.MFnDependencyNode()
        locator.create("locator")
        self.assertTrue(cmds.objExists(locator.name()))


if __name__ == "__main__":
    unittest.main()
