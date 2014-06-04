#-*- encoding: utf-8

import maya.cmds
import texture

class Material:

  def _listingMaterialNode(self):
    shapeNode = maya.cmds.listRelatives(self.transform, s=True, pa=True)
    shadingGroupsBuf = maya.cmds.listConnections(t="shadingEngine")
    shadingGroups = list(set(shadingGroupsBuf))
    materialNames = []
    for sg in shadingGroups:
      if sg != "initialShadingGroup":
        materialNames.append(sg[:-2])
    return materialNames


  def _listingFacesFromMaterial(self):
    materialToFaces = {}
    for m in materials:
      maya.cmds.select(transform)
      maya.cmds.hyperShade(m, o=True)
      maya.cmds.select(vis=True)
      targetFaces = maya.cmds.ls(sl=True, fl=True)
      materialToFaces[m] = targetFaces
    return materialToFaces


  def __init__(self, mmdData, transform, filePath):
    self.transform = transform
    self.mmdData = mmdData
    self.baseDirectory = filePath
    self.materialNames = self._listingMaterialNode()
    self.texture = texture.Texture(mmdData, self.materialNames, self.baseDirectory)

# hyperShade(objectName, o=True)