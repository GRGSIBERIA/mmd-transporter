#-*- encoding: utf-8
import maya.cmds
import maya.mel

import util

class MmdBlendShapeWindow:
  def __init__(self):
    try:
      self.transform = maya.cmds.ls(sl=True)[0]
    except:
      raise Exception("Do not select MMD transform object.")
    self.blendShapeNode = self._getBlendShape(self.transform)
    self.blendShapeWeights = self._getWeights(self.blendShapeNode)
    self.blendShapeGroups = self._getBlendShapeGroups(self.blendShapeNode, self.transform)
    self.blendShapeNames = self._getBlendShapeNames(self.blendShapeGroups)


  def _getBlendShape(self, transform):
    histories = maya.cmds.listHistory(transform)
    try:
      blendShape = maya.cmds.ls(histories, type="blendShape")[0]
    except:
      raise Exception("Do not have blendShape node selected transform.")
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


  def _callSelectBlendShapeNode(self):
    maya.cmds.select(self.blendShapeNode)


  def _menu(self):
    maya.cmds.menu(l="Option")
    maya.cmds.menuItem(l="Select BlendShape Node",\
      command=lambda *args:self._callSelectBlendShapeNode())

  def _changeFloatSlider(self, shape, floatValue):
    blendShapeName = "%s.%s" % (self.blendShapeNode, shape)
    maya.cmds.setAttr(blendShapeName, floatValue)


  def _setKeyFrame(self, shape):
    maya.cmds.setKeyframe("%s.%s" % (self.blendShapeNode, shape))


  def _drawBlendShapeLine(self, shape, jpName):
    floatValue = maya.cmds.getAttr("%s.%s" % (self.blendShapeNode, shape))
    maya.cmds.floatSliderGrp(\
      l=jpName, min=0, max=1, step=0.02, fmn=0, fmx=1, fs=0.02, \
      width=300, value=floatValue, field=True,\
      changeCommand=lambda *args:self._changeFloatSlider(shape, args[0]))
    maya.cmds.button(l="Key", w=48, command=lambda *args:self._setKeyFrame(shape))


  def _layout(self, window, blendShapeNames):
    #form = maya.cmds.formLayout(numberOfDivisions=100)
    scrollLayout = maya.cmds.scrollLayout(vst=16)
    maya.cmds.columnLayout(adj=True)
    for expType, shapes in blendShapeNames.items():
      maya.cmds.frameLayout(collapsable=True, l=expType)
      maya.cmds.rowColumnLayout(nc=2)
      for shape, jpName in shapes.items():
        self._drawBlendShapeLine(shape, jpName)
      maya.cmds.setParent("..")
      maya.cmds.setParent("..")


  def show(self):
    title = "MMD BlendShape Window"
    window = maya.cmds.window(\
      t=title, wh=(400, 800),\
      menuBar=True)

    self._menu()
    self._layout(window, self.blendShapeNames)
    #maya.cmds.showWindow()
    maya.cmds.dockControl(\
      l=title, content=window, area="left", allowedArea=("left", "right"))

w = MmdBlendShapeWindow()
w.show()
