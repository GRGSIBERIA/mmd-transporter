#-*- encoding: utf-8

class FaceMaterial:
  def __init__(self, splited):
    self.material = splited[1]
    self.index = int(splited[2])

class FaceMaterialImporter:
  def __init__(self, directory):
    self.directory = directory

  def importCSV():
    faces = []
    with open(self.directory + "/out_face_material.csv") as f:
      for line in f:
        splited = line.split(",")
        if splited[0] == "Face":
          self.faces.append(FaceMaterial(splited))
    return faces

class FaceMaterialGenerator:
  def __init__(self):
    pass