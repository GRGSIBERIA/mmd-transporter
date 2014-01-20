#-*- encoding: utf-8
import csv

class ImportFromCSV:
    def __init__(self):
      path = "C:/"
      self.vertices = ReadFrom3Float(path + "out_vertices.csv")
      self.normals = []
      self.indices = []

    def ReadFrom3Float(self, path):
      arr = []
      with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
          append_arr = [float(row[0]), float(row[1]), float(row[2])]
          arr.append(append_arr)
      return arr

    def ReadFrom3Int(self, path):
      arr = []
      with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
          append_arr = [int(row[0]), int(row[1]), int(row[2])]
          arr.append(append_arr)
      return arr