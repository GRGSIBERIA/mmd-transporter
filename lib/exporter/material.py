#-*- encoding: utf-8

import maya.cmds
import os.path
import sys
import shutil

class Material:

  def _listingMaterialNode(self):
    shapeNode = maya.cmds.listRelatives(self.transform, s=True, pa=True)
    shadingGroupsBuf = maya.cmds.listConnections(t="shadingEngine")
    shadingGroups = list(set(shadingGroupsBuf))
    self.materialNames = []
    for sg in shadingGroups:
      if sg != "initialShadingGroup":
        self.materialNames.append(sg[:-2])


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
    self._listingMaterialNode()

# hyperShade(objectName, o=True)