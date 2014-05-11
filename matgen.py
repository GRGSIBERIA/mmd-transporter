#-*- encoding: utf-8
import sys
import os.path
import maya.OpenMayaMPx
import maya.cmds as cmds

class MaterialGenerator:
  def __init__(self, mmdData, filePath):
    self.mmdData = mmdData
    self.directory = os.path.dirname(filePath)

  def _createMaterialNode(self, materialData):
    materialName = materialData.english_name
    material = None
    if materialName != "":
      material = cmds.shadingNode("blinn", asShader=1, name='%s' % materialName)
    else:
      material = cmds.shadingNode("blinn", asShader=1)

    shader_group = cmds.sets(renderable=1, noSurfaceShader=1, empty=1, name='%sSG' % material)
    #cmds.sets(model, e=1, forceElement=shader_group)   # ここは無視しておこう
    cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % shader_group, f=1)
    return material, shader_group

  def _getFileName(self, path):
    return os.path.basename(path)

  def _createFileNode(self, texturePath):
    file_node = cmds.shadingNode("file", asTexture=1)
    placed2d  = cmds.shadingNode("place2dTexture", asUtility=1)
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

  def _setMaterial(self, mat_node, file_node, material):
    cmds.setAttr("%s.transparency" % mat_node, material.alpha, material.alpha, material.alpha, type="double3")
    cmds.setAttr("%s.ambientColor" % mat_node, material.ambient_color[0], material.ambient_color[1], material.ambient_color[2], type="double3")
    cmds.setAttr("%s.specularColor" % mat_node, material.specular_color[0], material.specular_color[1], material.specular_color[2], type="double3")
    cmds.setAttr("%s.eccentricity" % mat_node, material.specular_factor * 0.01)
    cmds.setAttr("%s.specularRollOff" % mat_node, material.specular_factor * 0.01)

    if material.texture != "":
      cmds.connectAttr("%s.outColor" % file_node ,"%s.color" % mat_node)
    else:
      cmds.setAttr("%s.color" % mat_node, material.diffuse_color[0], material.diffuse_color[1], material.diffuse_color[2], type="double3")

    ext = os.path.splitext(material.texture)[1]
    if ext == ".png" or ext == ".tga":
      if cmds.getAttr("%s.fileHasAlpha" % file_node) == 1:
        cmds.connectAttr("%s.outTransparency" % file_node, "%s.transparency" % mat_node)


  def generate(self):
    fileNodeNames = []
    for i in range(len(self.mmdData.textures)):
      fileNode = self._createFileNode(self.mmdData.textures[i])
      fileNodeNames.append(fileNode)
      self._setTexture(fileNode, self.mmdData.textures[i])

    shaderGroupNodes = []
    for i in range(len(self.mmdData.materials)):
      material = self.mmdData.materials[i]
      materialNode, shaderGroup = self._createMaterialNode(material)
      fileNode = fileNodeNames[material.texture_index]
      self._setMaterial(materialNode, fileNode, material)
      materialNodes.append(materialNode)
      shaderGroupNodes.append(shaderGroup)
    return shaderGroupNodes