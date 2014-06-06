#-*- encoding: utf-8

import maya.cmds
import maya.mel
import texture

import pymeshio.common
import pymeshio.pmx

class Material:

  def _listingMaterialNode(self):
    shapeNode = maya.cmds.listRelatives(self.transform, s=True, pa=True)
    shadingGroupsBuf = maya.cmds.listConnections(shapeNode[0], t="shadingEngine")
    shadingGroups = list(set(shadingGroupsBuf))
    materialNames = []
    for sg in shadingGroups:
      if sg != "initialShadingGroup":
        materialNames.append(sg[:-2])
    return materialNames


  def _listingFacesFromMaterial(self):
    materialToFaces = {}
    for m in self.materialNames:
      maya.cmds.select(self.transform)
      #maya.cmds.hyperShade(m, o=True)
      maya.mel.eval("hyperShade -o %s" % m)
      maya.cmds.select(vis=True)
      targetFaces = maya.cmds.ls(sl=True, fl=True)
      materialToFaces[m] = targetFaces
    return materialToFaces


  def _listingOrderToMaterial(self):
    orderToMaterial = {}
    for m in self.materialNames:
      order = maya.cmds.getAttr("%s.drawOrder" % m)
      orderToMaterial[order] = m
    return orderToMaterial


  def _getDiffuseColor(self, m):
    buf = maya.cmds.listConnections("%s.color" % m)
    if len(buf) > 0:
      diffuseFactor = maya.cmds.getAttr("%s.diffuse" % m)
      diffuseColor = [diffuseFactor, diffuseFactor, diffuseFactor]
    else:
      diffuseColor = maya.cmds.getAttr("%s.color" % m)[0]
    return diffuseColor


  def _getAlpha(self, m):
    textureIndex = self.texture.materialNameToIndex[m]
    textureName = self.texture.textureNames[textureIndex]
    hasAlpha = maya.cmds.getAttr("%s.fileHasAlpha" % textureName)
    if hasAlpha == 1:
      return 0.98
    alpha = maya.cmds.getAttr("%s.transparency" % m)[0]
    return (alpha[0] + alpha[1] + alpha[2]) / 3.0


  def _toRGB(self, l):
    return pymeshio.common.RGB(l[0], l[1], l[2])


  def _getTexture(self, materialName):
    return self.texture.materialNameToIndex[materialName]


  def _createMaterials(self):
    for i in range(len(self.materialNames)):
      materialName = self.orderToMaterial[i]
      materialInst = pymeshio.pmx.Material(\
        name=maya.cmds.getAttr("%s.jpName" % materialName),
        english_name=materialName,
        diffuse_color=self._toRGB(self._getDiffuseColor(materialName)),
        alpha=self._getAlpha(materialName),
        specular_factor=maya.cmds.getAttr("%s.eccentricity" % materialName) * 100,
        specular_color=self._toRGB(maya.cmds.getAttr("%s.specularColor" % materialName)[0]),
        ambient_color=self._toRGB(maya.cmds.getAttr("%s.ambientColor" % materialName)[0]),
        flag=pymeshio.pmx.MATERIALFLAG_BOTHFACE+pymeshio.pmx.MATERIALFLAG_GROUNDSHADOW+pymeshio.pmx.MATERIALFLAG_SELFSHADOW+pymeshio.pmx.MATERIALFLAG_SELFSHADOWMAP,
        edge_color=pymeshio.common.RGBA(0, 0, 0, 0),
        edge_size=0.0,
        texture_index=self._getTexture(materialName),
        sphere_texture_index=0,
        sphere_mode=pymeshio.pmx.MATERIALSPHERE_NONE,
        toon_sharing_flag=False,    # toon_shading_flagじゃないのコレ？
        toon_texture_index=0,
        comment="",
        vertex_count=len(self.materialToFaces[materialName]))
      self.mmdData.materials.append(materialInst)


  def __init__(self, mmdData, transform, filePath):
    self.transform = transform
    self.mmdData = mmdData
    self.baseDirectory = filePath
    self.materialNames = self._listingMaterialNode()
    self.orderToMaterial = self._listingOrderToMaterial()
    self.texture = texture.Texture(mmdData, self.materialNames, self.baseDirectory)
    self.orderToMaterial = self._listingOrderToMaterial()
    self.materialToFaces = self._listingFacesFromMaterial()
    self._createMaterials()
