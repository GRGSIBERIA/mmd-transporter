#-*- encoding: utf-8
import sys
import os
import maya.OpenMaya
import maya.OpenMayaMPx
import maya.cmds as cmds

from transporter import *
from loadmmd_command import *

# directory = cmds.fileDialog2(dialogStyle=2, fileMode=3, okCaption="Select")


kPluginNodeName = 'transportedMMD1'
kPluginNodeId = maya.OpenMaya.MTypeId(0x03939)

kPluginCmdName = "loadmmd"


def initializePlugin(mobject):
  mplugin = maya.OpenMayaMPx.MFnPlugin(mobject, "Eiichi Takebuchi", "1.0")
  try:
    mplugin.registerNode(kPluginNodeName, kPluginNodeId, MMDTransporter.nodeCreator, MMDTransporter.nodeInitializer)
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

