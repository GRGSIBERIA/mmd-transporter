#-*- encoding: utf-8
import maya.OpenMaya
import maya.OpenMayaMPx
import maya.cmds as cmds

from transporter import *

class LoadMMDCommand(maya.OpenMayaMPx.MPxCommand):
  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  @classmethod
  def cmdCreator(cls):
    return maya.OpenMayaMPx.asMPxPtr(cls())

  def doIt(self, args):
    csv_file_path = cmds.fileDialog2(dialogStyle=2, selectFileFilter="*.csv", okCaption="Select")[0]

    MMDTransporter.csvFilePath = csv_file_path
    poly = maya.cmds.createNode('transform')
    mesh = maya.cmds.createNode('mesh', parent=poly)
    maya.cmds.sets(mesh, add='initialShadingGroup')
    spoly = maya.cmds.createNode('transportedMMD1')
    maya.cmds.connectAttr(spoly + '.outputMesh', mesh + '.inMesh')

    records = CSVImporter().toRowList(csv_file_path)
    mg = MaterialGenerator(records, csv_file_path)
    shader_groups = mg.generate()
    fmg = FaceMaterialGenerator()
    fmg.generate(records, mesh, shader_groups)