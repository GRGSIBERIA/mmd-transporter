#-*- encoding: utf-8
import maya.cmds
import maya.mel

import util

class MmdBlendShapeWindow:
  def __init__(self):
    pass

  def _layout(self, window):
    maya.cmds.columnLayout()


  def _getBlendShapeGroups(self):
    mother = maya.cmds.ls(sl=True)[0]


  def show(self):
    window = maya.cmds.window(t="MMD BlendShape Window", wh=(200, 600))
    self._getBlendShapeGroups()
    self._layout(window)
    maya.cmds.showWindow()

w = MmdBlendShapeWindow()
w.show()