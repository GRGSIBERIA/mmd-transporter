#-*- encoding: utf-8
import sys
import os
import maya.OpenMaya
import maya.OpenMayaMPx
import maya.cmds as cmds

from transporter import *


# directory = cmds.fileDialog2(dialogStyle=2, fileMode=3, okCaption="Select")


kPluginNodeName = 'transportedMMD1'
kPluginNodeId = maya.OpenMaya.MTypeId(0x03939)

kPluginCmdName = "loadmmd"


def nodeCreator():
  csv_file_path = cmds.fileDialog2(dialogStyle=2, selectFileFilter="*.csv", okCaption="Select")[0]
  return maya.OpenMayaMPx.asMPxPtr(MMDTransporter(csv_file_path))


def nodeInitializer():
  nAttr = maya.OpenMaya.MFnNumericAttribute()
  MMDTransporter.widthHeight = nAttr.create('widthHeight', 'wh', maya.OpenMaya.MFnNumericData.kFloat, 1.0)
  nAttr.setStorable(1)

  typedAttr = maya.OpenMaya.MFnTypedAttribute()
  MMDTransporter.outputMesh = typedAttr.create('outputMesh', 'out', maya.OpenMaya.MFnData.kMesh)
  MMDTransporter.addAttribute(MMDTransporter.widthHeight)
  MMDTransporter.addAttribute(MMDTransporter.outputMesh)
  MMDTransporter.attributeAffects(MMDTransporter.widthHeight, MMDTransporter.outputMesh)


def initializePlugin(mobject):
  mplugin = maya.OpenMayaMPx.MFnPlugin(mobject, "Eiichi Takebuchi", "1.0")
  try:
    mplugin.registerNode(kPluginNodeName, kPluginNodeId, nodeCreator, nodeInitializer)
    mplugin.registerCommand(kPluginCmdName, LoadMMDCommand.cmdCreator)
  except:
    sys.stderr.write('Failed to register node: %s' % kPluginNodeName)
    raise


def uninitializePlugin(mobject):
  mplugin = maya.OpenMayaMPx.MFnPlugin(mobject)
  try:
    mplugin.deregisterNode(kPluginNodeId)
    mplugin.deregisterCommand(kPluginCmdName)
  except:
    sys.stderr.write('Failed to deregister node: %s' % kPluginNodeName)
    raise





def loadMMDTransporter():
  poly = maya.cmds.createNode('transform')
  mesh = maya.cmds.createNode('mesh', parent=poly)
  maya.cmds.sets(mesh, add='initialShadingGroup')
  spoly = maya.cmds.createNode('transportedMMD1')
  maya.cmds.connectAttr(spoly + '.outputMesh', mesh + '.inMesh') 