#-*- encoding: utf-8
# MMDのBlendShapeを効率的に扱うための窓

import maya.cmds
import maya.OpenMayaMPx

import bswindow
import blwindow

class MmdBlendShapeWindowCommand(maya.OpenMayaMPx.MPxCommand):

  @classmethod
  def commandCreator(cls):
    return maya.OpenMayaMPx.asMPxPtr(MmdBlendShapeWindowCommand())

  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  def doIt(self, args):
    window = bswindow.MmdBlendShapeWindow()
    window.show()


class MmdBoneListWindowCommand(maya.OpenMayaMPx.MPxCommand):

  @classmethod
  def commandCreator(cls):
    return maya.OpenMayaMPx.asMPxPtr(MmdBoneListWindowCommand())

  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  def doIt(self, args):
    window = blwindow.MmdBoneListWindow()
    window.show()


def registerCommands(mplugin):
  mplugin.registerCommand("mmdbswindow", MmdBlendShapeWindowCommand.commandCreator())
  mplugin.registerCommand("mmdblwindow", MmdBoneListWindowCommand.commandCreator())


def deregisterCommands(mplugin):
  mplugin.deregisterCommand("mmdbswindow")
  mplugin.deregisterCommand("mmdblwindow")