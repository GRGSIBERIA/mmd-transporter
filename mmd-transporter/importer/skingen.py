#-*- encoding: utf-8

import maya.OpenMaya
import maya.cmds

import pymeshio.pmx

class SkinGenerator:

  def __init__(self, mmdData):
    self.mmdData = mmdData


  def _getSkinFn(self, scluster):
    selectList = maya.OpenMaya.MSelectionList()
    selectList.add(scluster)
    clusterNode = maya.OpenMaya.MObject()
    selectList.getDependNode(0, clusterNode)
    return maya.OpenMayaAnim.MFnSkinCluster(clusterNode)


  def _normalizeSkinWeights(self, polyName, scluster, infIdPath):
    for inf in infIdPath.values():
      maya.cmds.setAttr("%s.liw" % inf)    # liw = lock influence weights

    skinNorm = maya.cmds.getAttr("%s.normalizeWeights" % scluster)
    if skinNorm:
      maya.cmds.setAttr("%s.normalizeWeights" % scluster, 0)
    maya.cmds.skinPercent(scluster, polyName, nrm=False, prw=100)

    if skinNorm:
      maya.cmds.setAttr("%s.normalizeWeights" % scluster, skinNorm)


  def _getWeightList(self, deform):
    if isinstance(self.mmdData, pymeshio.pmx.Model):
      if isinstance(deform, pymeshio.pmx.Bdef1):
        return \
          [deform.index0], \
          [1.0]
      elif isinstance(deform, pymeshio.pmx.Bdef2) or isinstance(deform, pymeshio.pmx.Sdef):
        return \
          [deform.index0, deform.index1], \
          [deform.weight0, 1.0-deform.weight0]
      elif isinstance(deform, pymeshio.pmx.Bdef4):
        return \
          [deform.index0, deform.index1, deform.index2, deform.index3], \
          [deform.weight0, deform.weight1, deform.weight2, deform.weight3]
    elif isinstance(self.mmdData, pymeshio.pmd.Model):
      return \
        [deform.index0, deform.index1], \
        [deform.weight0, 1.0-deform.weight0]


  def _useSetAttr(self, skinFn, scluster, inWeight, jointNames):
    weightListPlug = skinFn.findPlug("weightList")
    weightPlug = skinFn.findPlug("weights")

    print type(inWeight)

    vertices = self.mmdData.vertices
    bones = self.mmdData.bones
    for vtxId in range(weightListPlug.numElements()):
      deform = vertices[vtxId].deform
      indices, weights = self._getWeightList(deform)
      for bwi in range(len(indices)):
        if indices[bwi] != -1 and weights[bwi]:
          index = indices[bwi]
          targetJonit = jointNames[index]
          boneId = inWeight[targetJonit]
          maya.cmds.setAttr("%s.weightList[%s].weights[%s]" % (scluster, vtxId, boneId), weights[bwi])


  def generate(self, skinCluster, jointNames, polyName):
    skinFn = self._getSkinFn(skinCluster)
    infDags = maya.OpenMaya.MDagPathArray()
    skinFn.influenceObjects(infDags)

    infIdPath = {}
    inWeight = {}
    for x in range(infDags.length()):
      boneFullPath = infDags[x].fullPathName()
      infId = int(skinFn.indexForInfluenceObject(infDags[x]))
      infIdPath[infId] = boneFullPath

      jointName = boneFullPath.split("|")[-1]
      inWeight[jointName] = infId

    self._normalizeSkinWeights(polyName, skinCluster, infIdPath)
    self._useSetAttr(skinFn, skinCluster, inWeight, jointNames)