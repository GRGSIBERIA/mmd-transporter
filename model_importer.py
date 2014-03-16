#-*- encoding: utf-8
import csv

class ModelImporter:
  def __init__(self, records):
    self.vertices = self._GetElement3s(records, u"Vertex", "f", 2)
    self.normals = self._GetElement3s(records, u"Vertex", "f", 5)
    self.indices = self._GetElement3s(records, u"Face", "i", 3)

  def _ToFloat3(self, r, start_index):
    return [float(r[start_index]), float(r[start_index+1]), float(r[start_index+2])]

  def _ToInt3(self, r, start_index):
    return [int(r[start_index]), int(r[start_index+1]), int(r[start_index+2])]

  def _GetElement3s(self, records, rtype, atype, start_index):
    buf = []
    for r in records:
      if r[0].decode("utf-8") == rtype:
        if atype == "f":
          buf.append(self._ToFloat3(r, start_index))
        elif atype == "i":
          buf.extend(self._ToInt3(r, start_index))
    return buf
