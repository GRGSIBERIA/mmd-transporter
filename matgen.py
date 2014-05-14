#-*- encoding: utf-8
import sys
import os.path
import maya.OpenMayaMPx
import maya.cmds as cmds

import csv
import filemanager as filemng

class MaterialGenerator:

  def __init__(self, mmdData, filePath):
    self.mmdData = mmdData
    self.directory = os.path.dirname(filePath)
    self.nameDict, self.dictFlag = filemng.openCSV(self.directory, "materialdict.csv")

  def _createMaterialNode(self, materialData, index):
    materialName = "mmd_material"
    if self.dictFlag:
      materialName = self.nameDict[index]

    material = None
    try:
      material = cmds.shadingNode("blinn", asShader=1, name='%s' % materialName)
    except:
      material = cmds.shadingNode("blinn", asShader=1)  # 不正な名前のマテリアルはこれ

    shader_group = cmds.sets(renderable=1, noSurfaceShader=1, empty=1, name='%sSG' % material)
    #cmds.sets(model, e=1, forceElement=shader_group)   # ここは無視しておこう
    cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % shader_group, f=1)
    return material, shader_group

  def _getFileName(self, path):
    return os.path.basename(path)

  def _createFileNode(self, texturePath):
    fileName = os.path.splitext(texturePath)[0]
    fileName = os.path.basename(fileName)
    file_node = cmds.shadingNode("file", asTexture=1, name=fileName)
    placed2d  = cmds.shadingNode("place2dTexture", asUtility=1, name="%s_place2dTexture" % fileName)
    cmds.connectAttr("%s.coverage" % placed2d, "%s.coverage" % file_node, f=True)
    cmds.connectAttr("%s.translateFrame" % placed2d, "%s.translateFrame" % file_node, f=True)
    cmds.connectAttr("%s.rotateFrame" % placed2d, "%s.rotateFrame" % file_node, f=True)
    cmds.connectAttr("%s.mirrorU" % placed2d, "%s.mirrorU" % file_node, f=True)
    cmds.connectAttr("%s.mirrorV" % placed2d, "%s.mirrorV" % file_node, f=True)
    cmds.connectAttr("%s.stagger" % placed2d, "%s.stagger" % file_node, f=True)
    cmds.connectAttr("%s.wrapU" % placed2d, "%s.wrapU" % file_node, f=True)
    cmds.connectAttr("%s.wrapV" % placed2d, "%s.wrapV" % file_node, f=True)
    cmds.connectAttr("%s.repeatUV" % placed2d, "%s.repeatUV" % file_node, f=True)
    cmds.connectAttr("%s.offset" % placed2d, "%s.offset" % file_node, f=True)
    cmds.connectAttr("%s.rotateUV" % placed2d, "%s.rotateUV" % file_node, f=True)
    cmds.connectAttr("%s.noiseUV" % placed2d, "%s.noiseUV" % file_node, f=True)
    cmds.connectAttr("%s.vertexUvOne" % placed2d, "%s.vertexUvOne" % file_node, f=True)
    cmds.connectAttr("%s.vertexUvTwo" % placed2d, "%s.vertexUvTwo" % file_node, f=True)
    cmds.connectAttr("%s.vertexUvThree" % placed2d, "%s.vertexUvThree" % file_node, f=True)
    cmds.connectAttr("%s.vertexCameraOne" % placed2d, "%s.vertexCameraOne" % file_node, f=True)
    cmds.connectAttr("%s.outUV" % placed2d, "%s.uv" % file_node)
    cmds.connectAttr("%s.outUvFilterSize" % placed2d, "%s.uvFilterSize" % file_node)
    return file_node


  def _setTexture(self, fileNode, texturePath):
    cmds.setAttr("%s.fileTextureName" % fileNode, self.directory + "/" + texturePath, type="string")

  def _setTransparency(self, material, texturePath, mat_node, file_node):
    alpha = material.alpha
    if alpha < 1.0:
      cmds.setAttr("%s.transparency" % mat_node, alpha, alpha, alpha, type="double3")

    ext = os.path.splitext(texturePath)[1]
    if ext == ".png" or ext == ".tga":
      if cmds.getAttr("%s.fileHasAlpha" % file_node) == 1 and alpha == 1.0:
        cmds.connectAttr("%s.outTransparency" % file_node, "%s.transparency" % mat_node)

    

  def _setMaterial(self, mat_node, file_node, material, textures):
    cmds.setAttr("%s.ambientColor" % mat_node, material.ambient_color[0], material.ambient_color[1], material.ambient_color[2], type="double3")
    cmds.setAttr("%s.specularColor" % mat_node, material.specular_color[0], material.specular_color[1], material.specular_color[2], type="double3")
    cmds.setAttr("%s.eccentricity" % mat_node, material.specular_factor * 0.01)
    cmds.setAttr("%s.specularRollOff" % mat_node, material.specular_factor * 0.01)

    texturePath = textures[material.texture_index]
    if texturePath != "":
      cmds.connectAttr("%s.outColor" % file_node ,"%s.color" % mat_node)
    else:
      cmds.setAttr("%s.color" % mat_node, material.diffuse_color[0], material.diffuse_color[1], material.diffuse_color[2], type="double3")

    self._setTransparency(material, texturePath, mat_node, file_node)


  def _generateTextureFile(self):
    fileNodeNames = []
    for i in range(len(self.mmdData.textures)):
      fileNode = self._createFileNode(self.mmdData.textures[i])
      fileNodeNames.append(fileNode)
      self._setTexture(fileNode, self.mmdData.textures[i])
    return fileNodeNames

  def _generateMaterials(self, fileNodeNames):
    shaderGroupNodes = []
    for i in range(len(self.mmdData.materials)):
      material = self.mmdData.materials[i]
      materialNode, shaderGroup = self._createMaterialNode(material, i)
      fileNode = fileNodeNames[material.texture_index]
      self._setMaterial(materialNode, fileNode, material, self.mmdData.textures)
      shaderGroupNodes.append(shaderGroup)
    return shaderGroupNodes    

  def _setFaceMaterials(self, meshName, shaderGroupNodes):
    cnt = 0
    for i in range(len(self.mmdData.materials)):
      sg = shaderGroupNodes[i]
      material = self.mmdData.materials[i]
      faceNumber = material.vertex_count / 3
      start = cnt
      end = cnt + faceNumber
      targetFaceName = "%s.f[%s:%s]" % (meshName, start, end)
      cmds.sets(targetFaceName, forceElement=sg)
      cnt += faceNumber

  def generate(self, meshName):
    fileNodeNames = self._generateTextureFile()
    shaderGroupNodes = self._generateMaterials(fileNodeNames)
    self._setFaceMaterials(meshName, shaderGroupNodes)

