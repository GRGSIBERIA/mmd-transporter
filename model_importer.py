#-*- encoding: utf-8
import csv

class ModelImporter:
  # def __init__(self, path):
  #   self.vertices = self.ReadFrom3Float(path + "out_vertices.csv")
  #   self.normals  = self.ReadFrom3Float(path + "out_normals.csv")
  #   self.indices  = self.ReadFrom3Int(path + "out_indices.csv")

  # def ReadFrom3Float(self, path):
  #   arr = []
  #   with open(path, "r") as f:
  #     reader = csv.reader(f)
  #     for row in reader:
  #       if len(row) > 0:
  #         append_arr = [float(row[0]), float(row[1]), float(row[2])]
  #         arr.append(append_arr)
  #   return arr

  # def ReadFrom3Int(self, path):
  #   arr = []
  #   with open(path, "r") as f:
  #     reader = csv.reader(f)
  #     for row in reader:
  #       if len(row) > 0:
  #         arr.append(int(row[0]))
  #   return arr
  def __init__(self, path):
    with open(path, "r") as f:
      reader = csv.reader(f)
      for row in reader:
        pass