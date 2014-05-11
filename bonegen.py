#-*- encoding: utf-8

import maya.OpenMaya
import maya.OpenMayaMPx
import maya.cmds

class BoneGenerator:
  def __init__(self, mmdData):
    self.mmdData = mmdData

  def generate(self):
    bones = self.mmdData.bones
    # KAKASHI使う