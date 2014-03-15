#-*- encoding: utf-8
class Material:
  def __init__(self, splited):
    self.diffuse_color = self.to_floats(splited[3:6])
    self.reflect_color = self.to_floats(splited[7:9])
    self.reflectivity  = float(splited[10])
    self.ambient_color = self.to_floats(splited[11:13])
    self.texture = splited[26]

  def to_floats(self, arr):
    retarr = []
    for a in arr:
      retarr.append(float(a))
    return retarr


class MaterialImporter:
  def __init__(self, directory):
    self.directory = directory

  def importCSV(self):
    with open(self.directory + "out_material.csv") as f:
      dic = {}
      for line in f:
        splited = f.split(',')
        if splited[0] == "Material":
          mat_name = splited[1]
          dic[mat_name] = Material(splited)
    return dic


class MaterialGenerator:
  def __init__(self, directory):
    self.importer = MaterialImporter(directory)
    self.material_dict = self.importer.importCSV()

  def generate(self, model):
    for name, mat in self.material_dict.items():
      nodes = self.createNode(model, name)

  def createNode(self, model, name):
    material = cmds.shadingNode("blinn", asShader=1)
    shader_group = cmds.sets(renderable=1, noSurfaceShader=1, empty=1, name='%sSG' % material)
    cmds.sets(model, e=1, forceElement=shader_group)
    cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % shader_group, f=1)
    return [material, shader_group]