#-*- encoding: utf-8

import maya.cmds
import texture

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
      maya.cmds.select(transform)
      maya.cmds.hyperShade(m, o=True)
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
    textureIndex = self.material.texture.materialNameToIndex[m]
    textureName = self.material.texture.textures[textureIndex]
    hasAlpha = maya.cmds.getAttr("%s.fileHasAlpha" % textureName)
    if hasAlpha == 1:
      return 0.98
    return 1


  def _createMaterials(self):
    for i in range(len(self.materialNames)):
      materialName = self.orderToMaterial[i]
      jpName = maya.cmds.getAttr("%s.jpName" % materialName)
      engName = materialName
      diffuseColor = self._getDiffuseColor(materialName)
      alpha = self._getAlpha(materialName)
      specularFactor = maya.cmds.getAttr("%s.eccentricity" % materialName) * 100
      specularColor = maya.cmds.getAttr("%s.specularColor" % materialName)[0]
      ambientColor = maya.cmds.getAttr("%s.ambientColor" % materialName)[0]
      flag = pymeshio.pmx.MATERIALFLAG_BOTHFACE + pymeshio.pmx.MATERIALFLAG_GROUNDSHADOW + pymeshio.pmx.MATERIALFLAG_SELFSHADOW + pymeshio.pmx.MATERIALFLAG_SELFSHADOWMAP
      

  def __init__(self, mmdData, transform, filePath, material):
    self.transform = transform
    self.mmdData = mmdData
    self.baseDirectory = filePath
    self.material = material
    self.materialNames = self._listingMaterialNode()
    self.orderToMaterial = self._listingOrderToMaterial()
    self.texture = texture.Texture(mmdData, self.materialNames, self.baseDirectory)
    self.orderToMaterial = self._listingOrderToMaterial()
    self._createMaterials()

# hyperShade(objectName, o=True)