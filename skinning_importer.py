#-*- encoding: utf-8
class Weight:
  def __init__(self, index, target_bones, weight_values):
    self.index = index
    self.bones = target_bones
    self.weight_values = weight_values

class SkinningImporter:
  def __init__(self):
    pass

  def importCSV(self, records):
    for rows in records:
      if rows[0] == "Vertex":
        index = int(rows[1])

  def _getBones(self, rows):
    return [rows[28], rows[30], rows[32], rows[34]]

  def _getWeight(self, rows):
    return [float(rows[29]), float(rows[31]), float(rows[33]), float(rows[35])]