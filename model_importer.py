#-*- encoding: utf-8
import csv

class ModelImporter:
  def __init__(self, records):
    self.vertices = []
    self.normals = []
    self.indices = []
    self.us = []
    self.vs = []
    self._loadRecords(records)

  def _ToFloat3(self, r, start_index):
    return [float(r[start_index]), float(r[start_index+1]), float(r[start_index+2])]

  def _ToInt3(self, r, start_index):
    return [int(r[start_index]), int(r[start_index+1]), int(r[start_index+2])]

  def _loadRecords(self, records):
    for row in records:
      if row[0] == "Vertex":
        self.vertices.append(self._ToFloat3(row, 2))
        self.normals.append(self._ToFloat3(row, 5))
        self.us.append(float(row[9]))
        self.vs.append(-1.0 * float(row[10]))
      elif row[0] == "Face":
        self.indices.extend(self._ToInt3(row, 3))