#-*- encoding: utf-8
import maya.cmds
import maya.OpenMaya
import copy

class JointOrientAdjuster:

  def __init__(self):
    pass


#-----------------------------------------------------------------------
# GUIのイベント関係
#-----------------------------------------------------------------------


  def _checkSelectedNodeType(self, nodeType):
    try:
      targetName = maya.cmds.ls(sl=True)[0]
      nodeTypeBuf = maya.cmds.nodeType(targetName)
      if nodeType != nodeTypeBuf:
        raise
    except:
      raise u"Do not select %s." % nodeType
    return targetName


  def _createEmptyNode(self, name):
    position = maya.cmds.xform(q=True, t=True, ws=True)
    emptyNode = maya.cmds.CreateEmptyGroup()
    maya.cmds.xform(t=position, ws=True)
    name = maya.cmds.rename(emptyNode, name)
    return name


  def _assignEmpty(self):
    self._target = self._checkSelectedNodeType("joint")
    self._rootEmpty = self._createEmptyNode("JointOrientController")
    maya.cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)


  def _initializeList(self):
    # 対象の親と子のボーンを対象にする
    self._targetChildren = maya.cmds.listRelatives(self._target, c=True, typ="joint")

    maya.cmds.textScrollList(self._targetChildrenList, e=True, ra=True)
    for i in range(len(self._targetChildren)):
      maya.cmds.textScrollList(self._targetChildrenList, e=True, a=self._targetChildren[i])
    maya.cmds.textScrollList(self._targetChildrenList, e=True, sii=1)


  # プルダウンメニューにしたほうがいい→コマンド名わからない
  def _createAdjuster(self, *args):
    self._assignEmpty()
    self._initializeList()
    maya.cmds.textField(self._controllerName, e=True, text=self._target)
    maya.cmds.textField(self._adjusterName, e=True, text=self._rootEmpty)


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


#-----------------------------------------------------------------------
# レイアウト関係
#-----------------------------------------------------------------------


  def _layoutChildrenList(self):
    maya.cmds.rowLayout(nc=2)
    maya.cmds.text("Target     ")
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
      l="Secondary Axis  ", nrb=3, la3=axisArray, sl=3, 
      cw4=columnWidth,
      changeCommand=self._checkRadioButtonForJointUp)
    self._prevFront = 1
    self._prevAxis = 2


  def _layoutSide(self):
    columnWidth = [140, 64, 64]
    self._secondDirectionX = maya.cmds.radioButtonGrp(
      l="Secondary Orientation  ", nrb=2, la2=["Xup", "Xdown"], cw3=columnWidth)
    self._secondDirectionY = maya.cmds.radioButtonGrp(
      l="", scl=self._secondDirectionX, nrb=2, la2=["Yup", "Ydown"], cw3=columnWidth)
    self._secondDirectionZ = maya.cmds.radioButtonGrp(
      l="", scl=self._secondDirectionX, nrb=2, la2=["Zup", "Zdown"], cw3=columnWidth, sl=1)


  def _changeManualFlag(self, *args):
    manual = maya.cmds.checkBox(self._enableManual, q=True, v=True)
    world = maya.cmds.checkBox(self._worldFlag, q=True, v=True)
    flag = manual or world
    print flag
    flag = False if flag else True
    maya.cmds.textScrollList(self._targetChildrenList, e=True, enable=flag)
    maya.cmds.radioButtonGrp(self._jointFront, e=True, enable=flag)
    maya.cmds.radioButtonGrp(self._secondAxis, e=True, enable=flag)
    maya.cmds.radioButtonGrp(self._secondDirectionX, e=True, enable=flag)
    maya.cmds.radioButtonGrp(self._secondDirectionY, e=True, enable=flag)
    maya.cmds.radioButtonGrp(self._secondDirectionZ, e=True, enable=flag)


  def _layoutHeader(self):
    maya.cmds.columnLayout()
    maya.cmds.button(l="Assign Adjuster", w=308, h=32, command=self._createAdjuster)
    maya.cmds.separator(h=8)
    self._enableManual = maya.cmds.checkBox(l="Enable Manual Adjustment", v=False, changeCommand=self._changeManualFlag)
    self._worldFlag = maya.cmds.checkBox(l="Orient Joint to World", v=False, changeCommand=self._changeManualFlag)
    maya.cmds.separator(h=8)
    maya.cmds.rowLayout(nc=2)
    maya.cmds.text(l="Adjuster Name   ")
    self._adjusterName = maya.cmds.textField(text="", editable=False, w=150)
    maya.cmds.setParent("..")
    maya.cmds.rowLayout(nc=2)
    maya.cmds.text(l="Controller Name  ")
    self._controllerName = maya.cmds.textField(text="", editable=False, w=150)
    maya.cmds.setParent("..")
    maya.cmds.separator(h=8)


  def _layoutOptions(self):
    self._layoutChildrenList()
    maya.cmds.separator(h=8)
    self._layoutJointAxisRadioButtons()
    maya.cmds.separator(h=8)
    self._layoutSide()
    maya.cmds.separator(h=8)
    maya.cmds.button(l="Adjust", w=308, h=32, command=self._doAdjustment)


#-----------------------------------------------------------------------
# 実行関係
#-----------------------------------------------------------------------


  def _adjustManual(self):
    pass


  def _getPrimary(self, transformArray):
    primaryNum = maya.cmds.radioButtonGrp(self._jointFront, q=True, sl=True) - 1
    direction = maya.OpenMaya.MVector()
    target = maya.cmds.xform(self._target, q=True, ws=True, t=True)
    child = maya.cmds.xform(self._targetChildren, q=True, ws=True, t=True)
    direction.x = child[0] - target[0]
    direction.y = child[1] - target[1]
    direction.z = child[2] - target[2]
    direction.normalize()
    transformArray[primaryNum] = direction
    return direction


  def _getSecondaryNumber(self):
    return maya.cmds.radioButtonGrp(self._secondAxis, q=True, sl=True) - 1


  def _getSecondary(self, transformArray):
    selectionArray = []
    vector = maya.OpenMaya.MVector()
    selectionArray.append(maya.cmds.radioButtonGrp(self._secondDirectionX, q=True, sl=True))
    selectionArray.append(maya.cmds.radioButtonGrp(self._secondDirectionY, q=True, sl=True))
    selectionArray.append(maya.cmds.radioButtonGrp(self._secondDirectionZ, q=True, sl=True))
    if selectionArray[0] > 0:
      vector.x = 1.0
    elif selectionArray[1] > 0:
      vector.y = 1.0
    elif selectionArray[2] > 0:
      vector.z = 1.0

    for i in range(3):
      if selectionArray[i] > 0:
        if selectionArray[i] == 2:
          vector *= -1.0
        secondaryNumber = self._getSecondaryNumber()
        transformArray[secondaryNumber] = vector
        return vector
    raise u"Do not select secondary axis. What's happen?"


  def _getThird(self, transformArray, primary, secondary):
    third = primary ^ secondary
    for i in range(3):
      try:
        if transformArray[i] == None: # MVectorとNoneを比較すると落ちる
          transformArray[i] = third
          return third
      except ValueError:
        pass


  def _adjustSecondary(self, transformArray, primary, third):
    secondary = third ^ primary
    secondaryNumber = self._getSecondaryNumber()
    transformArray[secondaryNumber] = secondary


  def _createMatrix(self, transformArray):
    transform = maya.OpenMaya.MMatrix()
    for i in range(3):
      for j in range(3):
        # この部分でエラーを起こすので、生ポインタを使うしかない
        # 親ボーンのJoint Orientを蓄積するの忘れた
        # EulerRotationにして親子で足し算したほうがいいかも
        transform[i * 4 + j] = transformArray[i][j]   # 使えない
    return transform

  def _getTransformMatrix(self):
    transformArray = [None] * 3
    primary = self._getPrimary(transformArray)
    secondary = self._getSecondary(transformArray)
    third = self._getThird(transformArray, primary, secondary)
    self._adjustSecondary(transformArray, primary, third)
    
    return self._createMatrix(transformArray)


  def _getEulerRotation(self):
    transform = self._getTransformMatrix()
    rotationMatrix = maya.OpenMaya.MTransformationMatrix(transform)
    return rotationMatrix.eulerRotation()


  def _disconnectChildren(self):
    selectNumber = maya.cmds.textScrollList(self._targetChildrenList, q=True, sii=True)[0] - 1
    targetChild = self._targetChildren[selectNumber]
    for joint in self._targetChildren:
      maya.cmds.parent(joint, w=True)   # 対象の子ボーン以外の接続を外す


  def _reconnectChildren(self):
    for joint in self._targetChildren:
      maya.cmds.connectJoint(joint, self._target, pm=True)


  def _adjustUsingAxis(self):
    # 一度、対象のジョイント以外の接続を外してからOrient Jointを実行する
    transformMatrix = self._getTransformMatrix()
    targetChildren = self._disconnectChildren()
    if not maya.cmds.checkBox(self._worldFlag, q=True, v=True):
      # Freezeさせる
      maya.cmds.joint(self._target, e=True, o=[0, 0, 0], zso=True)
    else:
      eulerRotation = self._getEulerRotation()
      print eulerRotation
    self._reconnectChildren()


  def _doAdjustment(self, *args):
    if maya.cmds.checkBox(self._enableManual, q=True, v=True):
      self._adjustManual()
    else:
      self._adjustUsingAxis()
    maya.cmds.select(self._target)


  def _layout(self):
    self._layoutHeader()
    self._layoutOptions()
    

  def show(self):
    self.window = maya.cmds.window(t="Joint Orient Adjuster", w=300, h=300)

    self._layout()

    maya.cmds.showWindow(self.window)


def show():
  joa = JointOrientAdjuster()
  joa.show()

show()