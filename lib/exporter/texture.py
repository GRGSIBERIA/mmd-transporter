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


  def _constructMaterialNameToTextureName(self):
    materialNameToTextureName = {}
    for materialName in self.materialNames:
      textureName = self.getTextureName(materialName)
      materialNameToTextureName[materialName] = textureName
    return materialNameToTextureName


  def _constructTexturePath(self):
    materialToTexturePath = {}
    self._createDirectory()
    for materialName in self.materialNames:
      textureName = self.materialNameToTextureName[materialName]
      fullPath = self.getTextureFullPath(textureName)
      if fullPath != -1 and textureName != -1:
        fileName = os.path.basename(fullPath)
        texturePath = "tex/" + fileName
        materialToTexturePath[materialName] = texturePath
        # 保存先にファイルを移動させる
        shutil.copyfile(fullPath, self.baseDirectory + "/" + texturePath)
    return materialToTexturePath


  def _constructTexturePathToMaterial(self):
    texturePathToMaterialName = {}
    for materialName, texturePath in self.materialNameToTexturePath.items():
      if not texturePathToMaterialName.has_key(texturePath):
        texturePathToMaterialName[texturePath] = []
      texturePathToMaterialName[texturePath].append(materialName)
    return texturePathToMaterialName


  def _constructTexturePathToIndex(self):
    texturePathToIndex = {}
    textures = []
    cnt = 0
    for texturePath in self.texturePathToMaterialName.keys():
      texturePathToIndex[texturePath] = cnt
      textures.append(texturePath)
      cnt += 1
    return texturePathToIndex, textures


  def _constructMaterialToTextureIndex(self):
    materialToTextureIndex = {}
    for materialName in self.materialNames:
      texturePath = self.materialNameToTexturePath[materialName]
      textureIndex = self.texturePathToIndex[texturePath]
      materialToTextureIndex[materialName] = textureIndex
    return materialToTextureIndex


  def __init__(self, mmdData, materialNames, baseDirectory):
    self.baseDirectory = baseDirectory
    self.mmdData = mmdData
    self.materialNames = materialNames
    self.materialNameToTextureName = self._constructMaterialNameToTextureName()
    self.materialNameToTexturePath = self._constructTexturePath()
    self.texturePathToMaterialName = self._constructTexturePathToMaterial()
    self.texturePathToIndex, self.textures = self._constructTexturePathToIndex()
    self.materialNameToTextureIndex = self._constructMaterialToTextureIndex()

    # self.texturesはtexturePathToIndexを構築するところで作ってます
    self.mmdData.textures = self.textures