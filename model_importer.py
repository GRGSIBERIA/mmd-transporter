#-*- encoding: utf-8
import csv

class ModelImporter:
  def __init__(self, records):
    self.vertices = self._GetElement3s(records, u"Vertex", "f", 1, 2)
    self.normals = self._GetElement3s(records, u"Vertex", "f", 1, 5)
    self.indices = self._GetElement3s(records, u"Face", "i", 2, 3)
    self.us = self._GetSingles(records, u"Vertex", 1, 9)
    self.vs = self._GetSingles(records, u"Vertex", 1, 10)

  def _ToFloat3(self, r, start_index):
    return [float(r[start_index]), float(r[start_index+1]), float(r[start_index+2])]

  def _ToInt3(self, r, start_index):
    return [int(r[start_index]), int(r[start_index+1]), int(r[start_index+2])]

  def _GetElement3s(self, records, rtype, atype, ri, start_index):
    buf = []
    cnt = 0
    for r in records:
      if r[0].decode("utf-8") == rtype:
        index = int(r[ri])
        if atype == "f":
          buf.append(self._ToFloat3(r, start_index))
        elif atype == "i":
          buf.append(self._ToInt3(r, start_index))
        cnt += 1
    return buf

  def _GetSingles(self, records, rtype, ri, start_index):
    buf = []
    for r in records:
      if r[0] == rtype:
        index = int(r[ri])
        elem = float(r[start_index])
        buf.append(elem)
    return buf

