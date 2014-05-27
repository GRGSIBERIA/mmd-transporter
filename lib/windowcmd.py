#-*- encoding: utf-8
# MMDのBlendShapeを効率的に扱うための窓

import maya.cmds
import maya.OpenMayaMPx

import window.bswindow
import window.blwindow
import window.rawindow


class MmdBlendShapeWindowCommand(maya.OpenMayaMPx.MPxCommand):

  @classmethod
  def commandCreator(cls):
    return maya.OpenMayaMPx.asMPxPtr(MmdBlendShapeWindowCommand())

  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  def doIt(self, args):
    window = window.bswindow.MmdBlendShapeWindow()
    window.show()


class MmdBoneListWindowCommand(maya.OpenMayaMPx.MPxCommand):

  @classmethod
  def commandCreator(cls):
    return maya.OpenMayaMPx.asMPxPtr(MmdBoneListWindowCommand())

  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  def doIt(self, args):
    window = window.blwindow.MmdBoneListWindow()
    window.show()


class MmdRigidbodyAdjustWindowCommand(maya.OpenMayaMPx.MPxCommand):

  @classmethod
  def commandCreator(cls):
    return maya.OpenMayaMPx.asMPxPtr(MmdRigidbodyAdjustWindowCommand())

  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  def doIt(self, args):
    window = window.rawindow.MmdRigidbodyAdjustWindow()
    window.show()