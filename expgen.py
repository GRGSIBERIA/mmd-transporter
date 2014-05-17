#-*- encoding: utf-8

import os.path
import maya.cmds
import maya.OpenMaya

import filemanager

class ExpressionGenerator:

  def __init__(self, mmdData, filePath):
    self.mmdData = mmdData
    self.directory = os.path.dirname(filePath)
    self.nameDict, self.dictFlag = filemanager.openCSV(self.directory, "morphdict.csv")

  def _duplicateMesh(self):
    morphs = self.mmdData.morphs
    morphNames = []
    morphPanelCounts = [0, 0, 0, 0, 0]
    baseIndex = 0
    for i in range(len(morphs)):
      morph = morphs[i]
      if morph.panel == 0:
        baseIndex = i
        continue    # baseなので無視

      name = "expression"
      if self.dictFlag:
        name = "exp_" + self.nameDict[i]
      morphName = maya.cmds.duplicate(self.polyName, n=name)
      morphNames.append(morphName)

      morphPanelCounts[morph.panel] += 1
      count = morphPanelCounts[morph.panel]
      maya.cmds.select(morphName)
      maya.cmds.move(8 * count, morph.panel * 8, -(morph.panel * 8))
    return baseIndex, morphNames

  def generate(self, polyName):
    self.polyName = polyName

    baseIndex, morphNames = self._duplicateMesh()