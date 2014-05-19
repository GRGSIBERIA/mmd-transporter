#-*- encoding: utf-8
import maya.cmds
import maya.mel

import util

class MmdBlendShapeWindow:
  def __init__(self):
    pass

  def _layout(self, window):
    maya.cmds.columnLayout()


  def _getBlendShape(self, transform):
    histories = maya.cmds.listHistory(transform)
    blendShape = maya.cmds.ls(histories, type="blendShape")[0]
    return blendShape


  def _getWeights(self, blendShape):
    attributes = maya.cmds.listAttr(blendShape)
    weights = []
    for item in attributes:
      if item.find("panel_") >= 0:
        expName = item.replace("panel_", "exp_")
        weights.append(expName)
    return weights


  def _getBlendShapeGroups(self, blendShape, transform):
    parentGroup = maya.cmds.listRelatives(transform, p=True)
    children = maya.cmds.listRelatives(parentGroup, c=True)
    for c in children:
      try:
        nodeType = maya.cmds.getAttr("%s.nodeType" % c)
        if nodeType == "blendShapeGroup":
          blendShapeGroupName = c
          return maya.cmds.listRelatives(blendShapeGroupName, c=True)
      except:
        pass
    raise


  def _getBlendShapeNames(self, blendShapeGroups):
    blendShapeNames = {}  # {expressionType => {transform => jpName}
    for group in blendShapeGroups:
      expressionType = maya.cmds.getAttr("%s.expression" % group)
      blendShapeTransforms = maya.cmds.listRelatives(group)

      transformToJpName = {}
      for transform in blendShapeTransforms:
        jpName = maya.cmds.getAttr("%s.jpName" % transform)
        transformToJpName[transform] = jpName
      blendShapeNames[expressionType] = transformToJpName
    return blendShapeNames


  def show(self):
    window = maya.cmds.window(t="MMD BlendShape Window", wh=(200, 600))

    transform = maya.cmds.ls(sl=True)[0]
    blendShapeNode = self._getBlendShape(transform)
    blendShapeWeights = self._getWeights(blendShapeNode)
    blendShapeGroups = self._getBlendShapeGroups(blendShapeNode, transform)
    blendShapeNames = self._getBlendShapeNames(blendShapeGroups)

    self._layout(window)
    maya.cmds.showWindow()

#w = MmdBlendShapeWindow()
#w.show()