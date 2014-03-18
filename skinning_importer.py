#-*- encoding: utf-8
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