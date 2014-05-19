#-*- encoding: utf-8
import maya.cmds
import maya.mel

import util

class MmdBlendShapeWindow:
  def __init__(self):
    pass

  def _layout(self, window):
    maya.cmds.columnLayout()


  def _getBlendShape(self):
    polygon = maya.cmds.ls(sl=True)[0]
    histories = maya.cmds.listHistory(polygon)
    blendShape = maya.cmds.ls(histories, type="blendShape")
    return blendShape


  def _getWeights(self, blendShape):
    attributes = maya.cmds.listAttr(blendShape)
    weights = []
    for item in attributes:
      if item.find("exp_") >= 0:
        weights.append(item)
    return weights

  def show(self):
    window = maya.cmds.window(t="MMD BlendShape Window", wh=(200, 600))

    blendShapeNode = self._getBlendShape()
    blendShapeWeights = self._getWeights(blendShapeNode)
    print blendShapeWeights

    self._layout(window)
    maya.cmds.showWindow()
