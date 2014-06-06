#-*- encoding: utf-8

import maya.cmds
import os
import os.path
import sys
import shutil

class Texture:

  def _listingTextures(self, materialNames):
    textures = []
    self.textureNames = []
    materialNameToIndex = {}
    cnt = 0
    try:
      os.mkdir(self.baseDirectory + "/tex")
    except:
      print "Exist %s/tex" % self.baseDirectory
    for m in materialNames:
      fullPath = self.getTextureFullPath(m)
      if fullPath != -1:
        fileName = os.path.basename(fullPath)
        texturePath = "tex/" + fileName
        textures.append(texturePath)
        shutil.copyfile(fullPath, self.baseDirectory + "/" + texturePath)
        self.textureNames.append(self.getTextureName(m))
        materialNameToIndex[m] = cnt
        cnt += 1
    self.mmdData.textures = textures
    return materialNameToIndex


  def getTextureName(self, materialName):
    connectedColor = maya.cmds.listConnections("%s.color" % materialName, t="file")
    if len(connectedColor) > 0:
      texture = connectedColor[0]
      return texture
    return -1


  def getTextureFullPath(self, materialName):
    texture = self.getTextureName(materialName)
    if texture != -1:
      return maya.cmds.getAttr("%s.fileTextureName" % texture)
    return -1


  def __init__(self, mmdData, materialNames, baseDirectory):
    self.baseDirectory = baseDirectory
    self.mmdData = mmdData
    self.materialNameToIndex = self._listingTextures(materialNames)