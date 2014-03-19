#-*- encoding: utf-8
import maya.cmds as cmds
import maya.OpenMaya
import maya.OpenMayaAnim

class Weight:
  def __init__(self, target_bones, weight_values):
    self.bones = target_bones
    self.weight_values = weight_values
    self.length = len(self.bones)

class SkinningImporter:
  def __init__(self):
    pass

  def importCSV(self, records):
    bone_weights = []
    for rows in records:
      if rows[0] == "Vertex":
        bones = self._getBones(rows)
        weights = self._getWeight(rows)
        bone_weights.append(Weight(bones, weights))
    return bone_weights

  def _appendBone(self, bones, rows, num):
    if rows[num] != "" and float(rows[num+1]) > 0.0:
      bones.append(rows[num])

  def _appendWeight(self, weights, rows, num):
    v = float(rows[num])
    if v > 0:
      weights.append(v)

  def _getBones(self, rows):
    bones = [rows[28]]
    self._appendBone(bones, rows, 30)
    self._appendBone(bones, rows, 32)
    self._appendBone(bones, rows, 34)
    return bones

  def _getWeight(self, rows):
    weights = [float(rows[29])]
    self._appendWeight(weights, rows, 31)
    self._appendWeight(weights, rows, 33)
    self._appendWeight(weights, rows, 35)
    return weights

class SkinningGenerator:
  def __init__(self):
    pass

  def generate(self, records, bone_objs, bone_insts, transform, scluster):
    bone_weights = SkinningImporter().importCSV(records)

    skinFn = self._getSkinFn(scluster)

    infDags = maya.OpenMaya.MDagPathArray()
    skinFn.influenceObjects(infDags)

    infs = {}
    inWeight = {}
    obj_path = {}
    for x in range(infDags.length()):
      infPath = infDags[x].fullPathName()
      infId = int(skinFn.indexForInfluenceObject(infDags[x]))
      infs[infId] = infPath

      joint_name = infPath.split("|")[-1]
      inWeight[joint_name] = infId

    self._normalizeSkinWeights(transform, scluster, infs)

    #weightListPlug = skinFn.findPlug("weightList")
    #weightPlug = skinFn.findPlug("weights")
    #weightListAttr = weightListPlug.attribute()
    #weightAttr = weightPlug.attribute()

    ## bone_objsの中身 == infPathの最後尾のボーン名
    #print "bonenum: %s" % weightListPlug.numElements()
    #for i in range(weightListPlug.numElements()):
    #  print i
    #  cmds.setAttr("%s.weightList[0].weights[%s]" % (scluster, i), 1)

    #for vtxId in range(weightListPlug.numElements()):
    #  bones = bone_weights[vtxId].bones
    #  weights = bone_weights[vtxId].weight_values
    #  for infNum in range(len(bones)):
    #    maya_name = bone_insts[bones[infNum]].maya_name
    #    boneId = inWeight[maya_name]
    #    weight = weights[infNum]
    #    cmds.setAttr("%s.weightList[%s].weights[%s]" % (scluster, vtxId, boneId), weight)

    #skinPercentを使う
    for vtx_ind in range(len(bone_weights)):
      bw = bone_weights[vtx_ind]
      transform_value = []
      for bwi in range(bw.length):
        target_bone = bone_objs[bw.bones[bwi]]
        weight = bw.weight_values[bwi]
        if weight > 0.0:
          transform_value.append((target_bone, weight))
      cmds.skinPercent(scluster, "%s.vtx[%s]" % (transform, vtx_ind), transformValue=transform_value)
      # joint8 is not an influence object for this skin. #
      # 操作中心ボーンということが判明

  def _normalizeSkinWeights(self, transform, scluster, infs):
    for inf in infs.values():
      cmds.setAttr("%s.liw" % inf)    # liw = lock influence weights

    skinNorm = cmds.getAttr("%s.normalizeWeights" % scluster)
    if skinNorm:
      cmds.setAttr("%s.normalizeWeights" % scluster, 0)
    cmds.skinPercent(scluster, transform, nrm=False, prw=100)

    if skinNorm:
      cmds.setAttr("%s.normalizeWeights" % scluster, skinNorm)

  def _getSkinFn(self, scluster):
    selectList = maya.OpenMaya.MSelectionList()
    selectList.add(scluster)
    clusterNode = maya.OpenMaya.MObject()
    selectList.getDependNode(0, clusterNode)
    return maya.OpenMayaAnim.MFnSkinCluster(clusterNode)
