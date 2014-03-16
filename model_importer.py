#-*- encoding: utf-8
import csv

class ModelImporter:
  def __init__(self, records):
    self.vertices = self._GetElement3s(records, "Vertex", "f", 1, 2)
    self.normals = self._GetElement3s(records, "Vertex", "f", 1, 5)
    self.indices = self._GetElement3s(records, "Face", "i", 2, 3)
    self.us = self._GetSingles(records, "Vertex", 1, 9)
    self.vs = self._GetSingles(records, "Vertex", 1, 10)

  def _ToFloat3(self, r, start_index):
    return [float(r[start_index]), float(r[start_index+1]), float(r[start_index+2])]

  def _ToInt3(self, r, start_index):
    return [int(r[start_index]), int(r[start_index+1]), int(r[start_index+2])]

  def _SortBuffer(self, buf):
    arr = []
    for i, e in sorted(buf.items()):
      arr.append(e)
    return arr

  def _GetElement3s(self, records, rtype, atype, ri, start_index):
    buf = {}
    for r in records:
      if r[0] == rtype:
        index = int(r[ri])
        e3 = self._ToFloat3(r) if atype == "f" else self._ToInt3(r)
        buf[index] = e3
    return self._SortBuffer(buf)

  def _GetSingles(self, records, rtype, ri, start_index):
    buf = {}
    for r in records:
      if r[0] == rtype:
        index = int(r[ri])
        elem = float(r[start_index])
        buf[index] = elem
    return self._SortBuffer(buf)

