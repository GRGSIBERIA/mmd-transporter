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

  def _getBones(self, rows):
    return [rows[28], rows[30], rows[32], rows[34]]

  def _getWeight(self, rows):
    return [float(rows[29]), float(rows[31]), float(rows[33]), float(rows[35])]

class SkinningGenerator:
  def __init__(self):
    pass

  def generate(self, records, bone_objs, skin_cluster):
    bone_weights = SkinningImporter().importCSV(records)

    # skin cluster nodeからMayaのオブジェクトを抽出する
    skinFn = self._extractSkinClusterFn(skin_cluster)

  def _extractSkinClusterFn(self, skin_cluster):
    select_list = maya.OpenMaya.MSelectionList()
    select_list.add(skin_cluster)
    cluster_node = maya.OpenMaya.MObject()
    select_list.getDependNode(0, cluster_node)
    skinFn = maya.OpenMayaAnim.MFnSkinCluster(cluster_node)
    return skinFn