#-*- encoding: utf-8

import maya.cmds

class Establish:

  def _listupExpressions(self):
    rotateExpressions = {}
    translateExpressions = {}
    boneNameToParentName = {}
    for boneName in self.boneNames:
      estabFlag = False
      try:
        maya.cmds.select("%s_rotate_E" % boneName)
        rotateFactor = maya.cmds.getAttr("%s.rotateFactor" % boneName)
        rotateExpressions[boneName] = rotateFactor
        estabFlag = True
      except:
        pass
      try:
        maya.cmds.select("%s_translate_E" % boneName)
        translateFactor = maya.cmds.getAttr("%s.translateFactor" % boneName)
        translateExpressions[boneName] = translateFactor
        estabFlag = True
      except:
        pass
      if estabFlag:
        parentName = maya.cmds.getAttr("%s.establishParent" % boneName)
        boneNameToParentName[boneName] = parentName
    return rotateExpressions, translateExpressions, boneNameToParentName


  def __init__(self, boneGroup, boneNameList):
    self.boneGroup = boneGroup
    self.boneNames = boneNameList
    self.rotate, self.translate, self.boneNameToParentName = self._listupExpressions()


