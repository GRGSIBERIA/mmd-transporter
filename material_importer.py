#-*- encoding: utf-8
class Material:
  def __init__(self, splited):
    self.diffuse_color = self.to_floats(splited[2:5])
    self.reflect_color = self.to_floats(splited[6:8])
    self.reflectivity  = float(splited[9])
    self.ambient_color = self.to_floats(splited[10:12])
    self.texture = splited[25]

  def to_floats(self, arr):
    retarr = []
    for a in arr:
      retarr.append(float(a))
    return retarr


class MaterialImporter:
  def __init__(self):
    f = open("c:/out_material.csv")
    dic = {}
    for line in f:
      splited = f.split(',')
      mat_name = splited[0]
      dic[mat_name] = Material(splited)