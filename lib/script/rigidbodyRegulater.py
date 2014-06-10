import maya.cmds


class rigidbodyRegulaterWindow:

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