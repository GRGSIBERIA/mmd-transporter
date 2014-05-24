#-*- encoding: utf-8
# MMDのBlendShapeを効率的に扱うための窓

import maya.cmds
import maya.OpenMayaMPx

import bswindow

class MmdBlendShapeWindowCommand(maya.OpenMayaMPx.MPxCommand):

  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  def doIt(self, args):
    window = bswindow.MmdBlendShapeWindow()
    window.show()