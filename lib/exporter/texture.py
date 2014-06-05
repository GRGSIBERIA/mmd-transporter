#-*- encoding: utf-8

import maya.cmds
import os
import os.path
import sys
import shutil

class Texture:

  def _listingTextures(self, materialNames):
    textures = []
    materialNameToIndex = {}
    cnt = 0
    os.mkdir(self.baseDirectory + "/tex")
    for m in materialNames:
      fullPath = self.getTextureFullPath(m)
      if fullPath != -1:
        fileName = os.path.basename(fullPath)
        texturePath = "tex/" + fileName
        textures.append(texturePath)
        shutil.copyfile(fullPath, self.baseDirectory + "/" + texturePath)
        materialNameToIndex[m] = cnt
        cnt += 1
    self.mmdData.textures = textures
    return materialNameToIndex


  def getTextureFullPath(self, materialName):
    connectedColor = maya.cmds.listConnections("%s.color" % materialName, t="file")
    if len(connectedColor) > 0:
      texture = connectedColor[0]
      return maya.cmds.getAttr("%s.fileTextureName" % texture)
    return -1


  def getTextureIndex(self, materialName):
    path = self.getTextureFullPath(materialName)
    if path != -1:
      return textureToIndex[fullPath]
    return -1


  def __init__(self, mmdData, materialNames, baseDirectory):
    self.baseDirectory = baseDirectory
    self.mmdData = mmdData
    self.materialNameToIndex = self._listingTextures(materialNames)