#-*- encoding: utf-8

class FaceMaterial:
  def __init__(self, splited):
    self.material = splited[1]
    self.index = int(splited[2])


class FaceMaterialImporter:
  def __init__(self, directory):
    self.directory = directory

  def importCSV(self, lines):
    faces = []
    for splited in lines:
      if splited[0] == "Face":  # 材質ごとに;Face行が存在するためそれは無視する
        self.faces.append(FaceMaterial(splited))
    return faces


class FaceMaterialGenerator:
  def __init__(self, directory):
    self.importer = FaceMaterialImporter(directory)

  def generate(self, model, shader_groups):
    faces = self.importer.importCSV()
    self.setMaterial(model, shader_groups, faces)

  def setMaterial(self, model, shader_groups, faces):
    for f in faces:
      num = str(f.index)
      target_sg = shader_groups[f.material]
      cmds.sets("%s.f[%s]" % (model, num), e=1, forceElement=target_sg)