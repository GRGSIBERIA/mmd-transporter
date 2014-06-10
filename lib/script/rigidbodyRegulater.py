import maya.cmds
import string

class RigidbodyRegulaterWindow:

  def _getRigidbodyGroup(self):
    selection = maya.cmds.ls(sl=True)
    if len(selection) <= 0:
      raise StandardError, "Do not select 'rigidbodies' Group."
    elif len(selection) > 1:
      raise StandardError, "You most only select 'rigidbodies' Group."

    group = selection[0]
    nodeType = maya.cmds.getAttr("%s.nodeType" % group)
    if nodeType != "rigidbodyGroup":
      raise StandardError, "Do not select 'rigidbodies' Group."
    return group


  def _listingShapes(self):
    return maya.cmds.listRelatives(self.rigidbodyGroup, c=True)


  def _listingColliders(self):
    colliders = []
    for shape in self.rigidbodyShapes:
      collider = shape.replace("rcube_", "rigid_")
      colliders.append(collider)
    return colliders


  def __init__(self):
    self.rigidbodyGroup = self._getRigidbodyGroup()
    self.rigidbodyShapes = self._listingShapes()
    self.colliders = self._listingColliders()


  def _createDefaultName(self, label):
    attrName = label.replace(" ", "")
    return "default" + attrName


  def _createAttributeName(self, label):
    try:
      strs = label.split(" ")   # 空白文字を削除して、先頭文字を小文字にする
      strs[0] = strs[0].lower()
      attribute = strs[0] + strs[1]
    except:
      return label.lower()
    return attribute


  def _changeFloatField(self, defaultName, attributeName, value):
    for collider in self.colliders:
      try:
        defaultValue = maya.cmds.getAttr("%s.%s" % (collider, defaultName))
        maya.cmds.setAttr("%s.%s" % (collider, attributeName), defaultValue * value)
      except:
        pass  # lengthなど存在しないColliderもあるのでパス


  def _showLine(self, label):
    width = 150
    changeMehod = lambda *args:self._changeFloatField(defaultName, attributeName, args[0])
    defaultName = self._createDefaultName(label)
    attributeName = self._createAttributeName(label)
    maya.cmds.rowLayout(numberOfColumns=2, columnWidth2=(width, 200))
    maya.cmds.text(label=label,
      align="right",
      width=width-20)
    maya.cmds.floatField(v=1.0,
      changeCommand=changeMehod,
      dragCommand=changeMehod)
    maya.cmds.setParent("..")


  def _layout(self):
    maya.cmds.columnLayout()

    maya.cmds.frameLayout(l="Rigidbody Properties")
    self._showLine("Mass")
    self._showLine("Linear Damping")
    self._showLine("Angular Damping")
    self._showLine("Friction")
    self._showLine("Restitution")
    
    maya.cmds.frameLayout(l="Collider Properties")
    self._showLine("Length")
    self._showLine("Radius")
    self._showLine("ExtentsX")
    self._showLine("ExtentsY")
    self._showLine("ExtentsZ")

    # JointConstraintの設定をする

  def show(self):
    window = maya.cmds.window(t="Rigidbody Regulater", w=400, h=300)

    self._layout()

    maya.cmds.showWindow(window)

maya.cmds.select("rigidbodies")
w = RigidbodyRegulaterWindow()
w.show()