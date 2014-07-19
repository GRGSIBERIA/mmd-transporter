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
    self._rootEmpty = self._createEmptyNode("JointOrientController")
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
    maya.cmds.textField(self._controllerName, e=True, text=self._target)


  def _getJointUpFront(self):
    front = maya.cmds.radioButtonGrp(self._jointFront, q=True, sl=True)
    up = maya.cmds.radioButtonGrp(self._secondAxis, q=True, sl=True)
    return (front, up)


  def _checkRadioButtonForJointUp(self, *args):
    front, up = self._getJointUpFront()
    if front == up:
      maya.cmds.radioButtonGrp(self._secondAxis, e=True, sl=self._prevAxis)
    self._prevAxis = up


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
    columnWidth = [140, 64, 64, 64]
    self._jointFront = maya.cmds.radioButtonGrp(
      l="Joint Front  ", nrb=3, la3=axisArray, sl=1, 
      cw4=columnWidth,
      changeCommand=self._checkRadioButtonForJointFront)
    self._secondAxis = maya.cmds.radioButtonGrp(
      l="Second Axis  ", nrb=3, la3=axisArray, sl=3, 
      cw4=columnWidth,
      changeCommand=self._checkRadioButtonForJointUp)
    self._prevFront = 1
    self._prevAxis = 2


  def _layoutSide(self):
    columnWidth = [140, 64, 64]
    self._secondDirectionX = maya.cmds.radioButtonGrp(
      l="Second Direction  ", nrb=2, la2=["+X", "-X"], cw3=columnWidth)
    self._secondDirectionY = maya.cmds.radioButtonGrp(
      l="", scl=self._secondDirectionX, nrb=2, la2=["+Y", "-Y"], cw3=columnWidth)
    self._secondDirectionZ = maya.cmds.radioButtonGrp(
      l="", scl=self._secondDirectionX, nrb=2, la2=["+Z", "-Z"], cw3=columnWidth, sl=1)


  def _changeManualFlag(self, *args):
    flag = maya.cmds.checkBox(self._enableManual, q=True, v=True)
    flag = False if flag else True
    maya.cmds.textScrollList(self._targetChildrenList, e=True, enable=flag)
    maya.cmds.radioButtonGrp(self._jointFront, e=True, enable=flag)
    maya.cmds.radioButtonGrp(self._secondAxis, e=True, enable=flag)
    maya.cmds.radioButtonGrp(self._secondDirectionX, e=True, enable=flag)
    maya.cmds.radioButtonGrp(self._secondDirectionY, e=True, enable=flag)
    maya.cmds.radioButtonGrp(self._secondDirectionZ, e=True, enable=flag)


  def _layoutHeader(self):
    maya.cmds.columnLayout()
    maya.cmds.rowLayout(nc=2)
    maya.cmds.button(l="Assign Adjuster", w=100, h=32, command=self._createAdjuster)
    self._enableManual = maya.cmds.checkBox(l="Enable Manual Adjustment", v=False, changeCommand=self._changeManualFlag)
    maya.cmds.setParent("..")
    maya.cmds.rowLayout(nc=2)
    maya.cmds.text(l="Controller Name  ")
    self._controllerName = maya.cmds.textField(text="", editable=False)
    maya.cmds.setParent("..")


  def _layoutOptions(self):
    self._layoutChildrenList()
    maya.cmds.separator(h=8)
    self._layoutJointAxisRadioButtons()
    maya.cmds.separator(h=8)
    self._layoutSide()


  def _adjustManual(self):
    pass



  def _testDirection(self, direction, axis):
    if direction != 0:
      if direction == 1:
        return 1.0
      return -1.0
    return 0.0


  def _getSecondaryDirection(self):
    dirX = maya.cmds.radioButtonGrp(self._secondDirectionX, q=True, sl=True)
    dirY = maya.cmds.radioButtonGrp(self._secondDirectionY, q=True, sl=True)
    dirZ = maya.cmds.radioButtonGrp(self._secondDirectionZ, q=True, sl=True)
    direction = maya.OpenMaya.MVector()
    direction.x = self._testDirection(dirX, "X")
    direction.y = self._testDirection(dirY, "Y")
    direction.z = self._testDirection(dirZ, "Z")
    return direction


  def _adjustUsingAxis(self):
    primary = maya.cmds.radioButtonGrp(self._jointFront, q=True, sl=True)
    second = maya.cmds.radioButtonGrp(self._secondAxis, q=True, sl=True)
    direction = self._getSecondaryDirection()


  def _doAdjustment(self, *args):
    if maya.cmds.checkBox(self._enableManual, q=True, v=True):
      self._adjustManual()
    self._adjustUsingAxis()
    

  def _layout(self):
    self._layoutHeader()
    self._layoutOptions()
    maya.cmds.button(l="Adjust", w=60, h=32, command=self._doAdjustment)
    

  def show(self):
    self.window = maya.cmds.window(t="Joint Orient Adjuster", w=400, h=300)

    self._layout()

    maya.cmds.showWindow(self.window)


def show():
  joa = JointOrientAdjuster()
  joa.show()

show()