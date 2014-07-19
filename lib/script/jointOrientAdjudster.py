#-*- encoding: utf-8
import maya.cmds
import maya.OpenMaya

class JointOrientAdjuster:
  def __init__(self):
    self._assignedFlag = False
    self._childJointCount = 0

  def _checkSelectedNodeType(self, nodeType):
    try:
      targetName = maya.cmds.ls(sl=True)[0]
      nodeType = maya.cmds.nodeType(targetName)
      if nodeType != nodeType:
        raise
    except:
      raise StandardError("Do not select %s." % nodeType)
    return targetName


  def _createEmptyNode(self, name):
    position = maya.cmds.xform(q=True, t=True, ws=True)
    emptyNode = maya.cmds.CreateEmptyGroup()
    maya.cmds.xform(t=position, ws=True)
    maya.cmds.rename(emptyNode, name)
    return name


  def _assignEmpty(self):
    self._target = self._checkSelectedNodeType("joint")
    self._rootEmpty = self._createEmptyNode("JointOrientAdjuster")
    self._assignedFlag = True
    maya.cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)


  # プルダウンメニューにしたほうがいい
  def _createAdjuster(self, *args):
    self._assignEmpty()
    self._targetChildren = maya.cmds.listRelatives(self._target, c=True, typ="joint")
    if self._targetChildren == None:
      self._targetChildren = ["None"]
    self._childJointCount = len(self._targetChildren)
    self._targetChildIndex = 0
    maya.cmds.textField(self._targetField, e=True, tx=self._targetChildren[0])


  def _getTargetChild(self):
    return self._targetChildren[self._targetChildIndex]


  def _changeTargetFieldText(self):
    maya.cmds.textField(self._targetField, e=True, tx=self._getTargetChild())


  def _prevChildJoint(self, *args):
    self._targetChildIndex -= 1
    if self._targetChildIndex < 0:
      self._targetChildIndex = self._childJointCount - 1
    self._changeTargetFieldText()


  def _nextChildJoint(self, *args):
    self._targetChildIndex += 1
    if self._targetChildIndex >= self._childJointCount:
      self._targetChildIndex = 0
    self._changeTargetFieldText()


  def _layout(self):
    maya.cmds.columnLayout()
    maya.cmds.button(l="Assign Adjuster", command=self._createAdjuster)

    maya.cmds.rowLayout(nc=4)
    maya.cmds.text("Target Child  ")
    self._targetField = maya.cmds.textField(editable=False)
    maya.cmds.button(l="<", command=self._prevChildJoint)
    maya.cmds.button(l=">", command=self._nextChildJoint)
    maya.cmds.setParent("..")

    maya.cmds.rowLayout(nc=4)
    maya.cmds.text("Orient Front  ")
    maya.cmds.button(l="X", w=24)
    maya.cmds.button(l="Y", w=24)
    maya.cmds.button(l="Z", w=24)
    maya.cmds.setParent("..")


  def show(self):
    self.window = maya.cmds.window(t="Joint Orient Adjuster", w=400, h=300)

    self._layout()

    maya.cmds.showWindow(self.window)


def show():
  joa = JointOrientAdjuster()
  joa.show()

show()