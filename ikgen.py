#-*- encoding: utf-8

import maya.OpenMaya
import maya.cmds

class IkGenerator:

  def __init__(self, mmdData):
    self.mmdData = mmdData


  def _createIk(self, jointNames, bone, bones):
    pass


  def generate(self, jointNames, humanIkFlag):
    if !humanIkFlag:
      bones = self.mmdData.bones
      for i in range(len(jointNames)):
        if jointNames[i] == "this_is_ik":
          self._createIk(jointNames, bones[i], bones)