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

  def createTexture(self, material):
    file_node = cmds.shadingNode("file", asTexture=1)
    placed2d  = cmds.shadingNode("place2dTexture", asUtility=1)
    cmds.connectAttr(f=True, "%s.coverage" % placed2d, "%s.coverage" % file_node)
    cmds.connectAttr(f=True, "%s.translateFrame" % placed2d, "%s.translateFrame" % file_node)
    cmds.connectAttr(f=True, "%s.rotateFrame" % placed2d, "%s.rotateFrame" % file_node)
    cmds.connectAttr(f=True, "%s.mirrorU" % placed2d, "%s.mirrorU" % file_node)
    cmds.connectAttr(f=True, "%s.mirrorV" % placed2d, "%s.mirrorV" % file_node)
    cmds.connectAttr(f=True, "%s.stagger" % placed2d, "%s.stagger" % file_node)
    cmds.connectAttr(f=True, "%s.wrapU" % placed2d, "%s.wrapU" % file_node)
    cmds.connectAttr(f=True, "%s.wrapV" % placed2d, "%s.wrapV" % file_node)
    cmds.connectAttr(f=True, "%s.repeatUV" % placed2d, "%s.repeatUV" % file_node)
    cmds.connectAttr(f=True, "%s.offset" % placed2d, "%s.offset" % file_node)
    cmds.connectAttr(f=True, "%s.rotateUV" % placed2d, "%s.rotateUV" % file_node)
    cmds.connectAttr(f=True, "%s.noiseUV" % placed2d, "%s.noiseUV" % file_node)
    cmds.connectAttr(f=True, "%s.vertexUvOne" % placed2d, "%s.vertexUvOne" % file_node)
    cmds.connectAttr(f=True, "%s.vertexUvTwo" % placed2d, "%s.vertexUvTwo" % file_node)
    cmds.connectAttr(f=True, "%s.vertexUvThree" % placed2d, "%s.vertexUvThree" % file_node)
    cmds.connectAttr(f=True, "%s.vertexCameraOne" % placed2d, "%s.vertexCameraOne" % file_node)
    cmds.connectAttr("%s.outUV" % placed2d, "%s.uv" % file_node)
    cmds.connectAttr("%s.outUvFilterSize", "%s.uvFi % placed2dlterSize" % file_node)