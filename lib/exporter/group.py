#-*- encoding: utf-8

import maya.cmds

import util

class Group:

  def _searchMother(self):
    selections = maya.cmds.ls(sl=True)
    if len(selections) <= 0:
      raise StandardError, "Do not select object."

    select = selections[0]
    mother = maya.cmds.listRelatives(select, p=True)[0]
    mmdFlag = util.getAttr(mother, "mmdModel")
    if not mmdFlag:
      raise StandardError, "Do not mmdModel Group"
    return (mother, select)


  def _divideGroups(self):
    motherChildren = maya.cmds.listRelatives(self.mother, c=True)
    for group in motherChildren:
      try:
        t = maya.cmds.getAttr("%s.nodeType" % group)
        if t == "rigidbodyGroup":
          self.rigidbody = group
        elif t == "constraintGroup":
          self.constraint = group
        elif t == "boneGroup":
          self.bone = group
      except:
        continue


  def _getBoneNames(self):
    boneNames = []
    children = maya.cmds.listRelatives(self.bone, c=True)
    for c in children:
      maya.cmds.select(c, hierarchy=True)
      boneNames += maya.cmds.ls(sl=True, type="joint")

    return boneNames


  def __init__(self):
    mother, transform = self._searchMother()
    self.mother = mother
    self.transform = transform
    self._divideGroups()
    self.boneNames = self._getBoneNames()