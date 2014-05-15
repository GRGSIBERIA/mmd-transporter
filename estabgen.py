#-*- encoding: utf-8

import maya.OpenMaya
import maya.cmds

class EstablishGenerator:
  
  def __init__(self, mmdData):
    self.mmdData = mmdData


  def generate(self, jointNames):
    bones = self.mmdData.bones
    for bone in bones:
      if bone.getExternalRotationFlag():
        pass

      if bone.getExternalTranslationFlag():
        pass