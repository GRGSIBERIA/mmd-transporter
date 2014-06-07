#-*- encoding: utf-8

import maya.cmds

class Establish:

  def _selectHierarchy(self):
    boneNames = []
    children = maya.cmds.listRelatives(self.boneGroup, c=True)
    for c in children:
      maya.cmds.select(c, hierarchy=True)
      boneNames += maya.cmds.ls(sl=True)


  def __init__(self, boneGroup):
    self.boneGroup = boneGroup