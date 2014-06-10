#-*- encoding: utf-8

import maya.cmds
import os
import os.path
import sys
import shutil

class Texture:

  def getTextureName(self, materialName):
    connectedColor = maya.cmds.listConnections("%s.color" % materialName, t="file")
    if len(connectedColor) > 0:
      texture = connectedColor[0]
      return texture
    return -1


  def getTextureFullPath(self, texture):
    if texture != -1:
      return maya.cmds.getAttr("%s.fileTextureName" % texture)
    return -1


  def _createDirectory(self):
    try:
      os.mkdir(self.baseDirectory + "/tex")
    except:
      print "Exist %s/tex" % self.baseDirectory


  def _constructTexturePath(self):
    materialToTexturePath = {}
    for materialName in self.materialNames:
      textureName = self.getTextureName(materialName)
      fullPath = self.getTextureFullPath(textureName)
      if fullPath != -1 and textureName != -1:
        fileName = os.path.basename(fullPath)
        texturePath = "tex/" + fileName
        materialToTexturePath[materialName] = texturePath
    return materialToTexturePath


  def _constructTexturePathToMaterial(self):
    texturePathToMaterialName = {}
    for materialName, texturePath in self.materialToTexturePath.items():
      if not texturePathToMaterialName.has_key(texturePath):
        texturePathToMaterialName[texturePath] = []
      texturePathToMaterialName[texturePath].append(materialName)
    return texturePathToMaterialName


  def _constructTexturePathToIndex(self):
    texturePathToIndex = {}
    cnt = 0
    for texturePath in self.texturePathToMaterialName.keys():
      texturePathToIndex[texturePath] = cnt
      cnt += 1
    return texturePathToIndex


  def _constructMaterialToTextureIndex(self):
    materialToTextureIndex = {}
    for materialName in self.materialNames:
      texturePath = self.materialToTexturePath[materialName]
      textureIndex = self.texturePathToIndex[texturePath]
      materialToTextureIndex[materialName] = textureIndex
    return materialToTextureIndex


  def _copyTextures(self):
    self._createDirectory()
    for texturePath in self.texturePathToMaterialName.keys():
      # 保存先にファイルを移動させる
      shutil.copyfile(fullPath, self.baseDirectory + "/" + texturePath)
        

  def __init__(self, mmdData, materialNames, baseDirectory):
    self.baseDirectory = baseDirectory
    self.mmdData = mmdData
    self.materialNames = materialNames
    self.materialToTexturePath = self._constructTexturePath()
    self.texturePathToMaterialName = self._constructTexturePathToMaterial()
    self.texturePathToIndex = self._constructTexturePathToIndex()
    self.materialToTextureIndex = self._constructMaterialToTextureIndex()
    self._copyTextures()