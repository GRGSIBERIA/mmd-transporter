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


  def _createAdjuster(self, *args):
    self._assignEmpty()
    self._childJointCount = len(maya.cmds.listRelatives(self._target, c=True, typ="joint"))
    maya.cmds.intField(self._childCountField, e=True, v=self._childJointCount)

  def _layout(self):
    maya.cmds.columnLayout()
    maya.cmds.button(l="Assign Adjuster", command=self._createAdjuster)
    maya.cmds.rowLayout(nc=2)
    maya.cmds.text("Number of Joint Children  ")
    self._childCountField = maya.cmds.intField(editable=False, v=self._childJointCount)
    maya.cmds.setParent("..")


  def show(self):
    self.window = maya.cmds.window(t="Joint Orient Adjuster", w=400, h=300)

    self._layout()

    maya.cmds.showWindow(self.window)


def show():
  joa = JointOrientAdjuster()
  joa.show()

show()