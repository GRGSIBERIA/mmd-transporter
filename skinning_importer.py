#-*- encoding: utf-8
import maya.OpenMaya
import maya.OpenMayaAnim

class Weight:
  def __init__(self, target_bones, weight_values):
    self.bones = target_bones
    self.weight_values = weight_values

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
    if rows[num] != "":
      bones.append(rows[num])

  def _appendWeight(self, weights, rows, num):
    if rows[num] != "0":
      weights.append(float(rows[num]))

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

  def generate(self, records, bone_objs, transform, scluster):
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
      inWeight[infPath] = infId
      joint_name = infPath.split("|")[-1]
      obj_path[joint_name] = infPath

    self._normalizeSkinWeights(transform, scluster, infs)

    weightListPlug = skinFn.findPlug("weightList")
    weightPlug = skinFn.findPlug("weights")
    weightListAttr = weightListPlug.attribute()
    weightAttr = weightPlug.attribute()

    # bone_objsの中身 == infPathの最後尾のボーン名
    for vtxId in range(weightListPlug.numElements()):
      bones = bone_weights[vtxId].bones
      weights = bone_weights[vtxId].weights
      for infNum in range(len(bones)):
        path = obj_path[bones[infNum]]
        boneId = inWeight[path]
        weight = weights[infNum]
        cmds.setAttr("%s.weightList[%s].weights[%s]" % (scluster, vtxId, boneId), weight)

  def _normalizeSkinWeights(self, transform, scluster, infs):
    for inf in infs.values():
      cmds.setAttr("%s.liw" % inf)    # liw = lock influence weights

    skinNorm = cmds.getAttr("%s.normalizeWeights" % scluster)
    if skinNorm:
      cmds.setAttr("%s.normalizeWeights", 0)
    cmds.skinPercent(scluster, transform, nrm=False, prw=0)

    if skinNorm:
      cmds.setAttr("%s.normalizeWeights" % scluster, skinNorm)

  def _getSkinFn(self, scluster):
    selectList = maya.OpenMaya.MSelectionList()
    selectList.add(scluster)
    clusterNode = maya.OpenMaya.MObject()
    selectList.getDependNode(0, clusterNode)
    skinFn = maya.OpenMayaAnim.MFnSkinCluster(clusterNode)