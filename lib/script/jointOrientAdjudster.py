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


  def _initializeList(self):
    self._targetChildren = maya.cmds.listRelatives(self._target, c=True, typ="joint")
    if self._targetChildren == None:
      self._targetChildren = ["None"]
    for i in range(len(self._targetChildren)):
      maya.cmds.textScrollList(self._targetChildrenList, e=True, a=self._targetChildren[i])
    maya.cmds.textScrollList(self._targetChildrenList, e=True, sii=1)


  # プルダウンメニューにしたほうがいい→コマンド名わからない
  def _createAdjuster(self, *args):
    self._assignEmpty()
    self._initializeList()


  def _getJointUpFront(self):
    front = maya.cmds.radioButtonGrp(self._jointFront, q=True, sl=True)
    up = maya.cmds.radioButtonGrp(self._jointUp, q=True, sl=True)
    return (front, up)


  def _checkRadioButtonForJointUp(self, *args):
    front, up = self._getJointUpFront()
    if front == up:
      maya.cmds.radioButtonGrp(self._jointUp, e=True, sl=self._prevUp)
    self._prevUp = up


  def _checkRadioButtonForJointFront(self, *args):
    front, up = self._getJointUpFront()
    if front == up:
      maya.cmds.radioButtonGrp(self._jointFront, e=True, sl=self._prevFront)
    self._prevFront = front


  def _layoutChildrenList(self):
    maya.cmds.rowLayout(nc=2)
    maya.cmds.text("Target Child  ")
    self._targetChildrenList = maya.cmds.textScrollList(h=100)
    maya.cmds.setParent("..")


  def _layoutJointAxisRadioButtons(self):
    # Joint Orientの向きを決めるためのもの
    axisArray = ["X", "Y", "Z"]
    self._jointFront = maya.cmds.radioButtonGrp(
      l="Joint Front", nrb=3, la3=axisArray, sl=1, changeCommand=self._checkRadioButtonForJointFront)
    self._jointUp = maya.cmds.radioButtonGrp(
      l="Joint Up", nrb=3, la3=axisArray, sl=2, changeCommand=self._checkRadioButtonForJointUp)
    self._prevFront = 1
    self._prevUp = 2


  def _layout(self):
    maya.cmds.columnLayout()
    maya.cmds.button(l="Assign Adjuster", command=self._createAdjuster)

    self._layoutChildrenList()
    self._layoutJointAxisRadioButtons()
    

  def show(self):
    self.window = maya.cmds.window(t="Joint Orient Adjuster", w=400, h=300)

    self._layout()

    maya.cmds.showWindow(self.window)


def show():
  joa = JointOrientAdjuster()
  joa.show()

show()