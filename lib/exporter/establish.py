#-*- encoding: utf-8

import maya.cmds

class Establish:

  def _listupExpressions(self):
    rotateExpressions = {}
    translateExpressions = {}
    for boneName in self.boneNames:
      try:
        maya.cmds.select("%s_rotate_E" % boneName)
        rotateExpressions[boneName] = True #rotateFactor
      except:
        pass
      try:
        maya.cmds.select("%s_translate_E" % boneName)
        translateExpressions[boneName] = True #translateFactor
      except:
        pass
    return rotateExpressions, translateExpressions


  def __init__(self, boneGroup, boneNameList):
    self.boneGroup = boneGroup
    self.boneNames = boneNameList
    self.rotate, self.translate = self._listupExpressions()


