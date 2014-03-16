#-*- encoding: utf-8
class Material:
  def __init__(self, splited):
    self.diffuse_color  = self.to_floats(splited[3:6])
    self.transparent    = 1.0 - float(splited[6])   # 0が透明
    self.specular_color = self.to_floats(splited[7:10])
    self.specularity    = float(splited[10])
    self.ambient_color  = self.to_floats(splited[11:14])
    self.texture = splited[26]

  def to_floats(self, arr):
    retarr = []
    for a in arr:
      retarr.append(float(a))
    return retarr


class MaterialImporter:
  def __init__(self, directory):
    self.directory = directory

  def importCSV(self, lines):
    dic = {}
    for splited in lines:
      if splited[0] == "Material":
        mat_name = splited[1]
        dic[mat_name] = Material(splited)
    return dic


class MaterialGenerator:
  def __init__(self, directory):
    self.directory = directory
    self.importer = MaterialImporter(directory)
    self.material_dict = self.importer.importCSV()

  # ShaderGroupを返す，SGはcmds.setsで利用する
  def generate(self):
    shader_group_for_mesh = {}
    for name, mat in self.material_dict.items():
      material_node, shader_group = self.createNode(model, name)
      file_node = self.createTexture()
      self.setTexture(file_node, mat)
      self.setMaterial(material_node, file_node, mat)
      shader_group_for_mesh[name] = shader_group
    return shader_group_for_mesh

  def createNode(self, model, name):
    material = cmds.shadingNode("blinn", asShader=1)
    shader_group = cmds.sets(renderable=1, noSurfaceShader=1, empty=1, name='%sSG' % material)
    #cmds.sets(model, e=1, forceElement=shader_group)   # ここは無視しておこう
    cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % shader_group, f=1)
    return material, shader_group

  def createTexture(self):
    file_node = cmds.shadingNode("file", asTexture=1)
    placed2d  = cmds.shadingNode("place2dTexture", asUtility=1)
    cmds.connectAttr("%s.coverage" % placed2d, "%s.coverage" % file_node, f=True)
    cmds.connectAttr("%s.translateFrame" % placed2d, "%s.translateFrame" % file_node, f=True)
    cmds.connectAttr("%s.rotateFrame" % placed2d, "%s.rotateFrame" % file_node, f=True)
    cmds.connectAttr("%s.mirrorU" % placed2d, "%s.mirrorU" % file_node, f=True)
    cmds.connectAttr("%s.mirrorV" % placed2d, "%s.mirrorV" % file_node, f=True)
    cmds.connectAttr("%s.stagger" % placed2d, "%s.stagger" % file_node, f=True)
    cmds.connectAttr("%s.wrapU" % placed2d, "%s.wrapU" % file_node, f=True)
    cmds.connectAttr("%s.wrapV" % placed2d, "%s.wrapV" % file_node, f=True)
    cmds.connectAttr("%s.repeatUV" % placed2d, "%s.repeatUV" % file_node, f=True)
    cmds.connectAttr("%s.offset" % placed2d, "%s.offset" % file_node, f=True)
    cmds.connectAttr("%s.rotateUV" % placed2d, "%s.rotateUV" % file_node, f=True)
    cmds.connectAttr("%s.noiseUV" % placed2d, "%s.noiseUV" % file_node, f=True)
    cmds.connectAttr("%s.vertexUvOne" % placed2d, "%s.vertexUvOne" % file_node, f=True)
    cmds.connectAttr("%s.vertexUvTwo" % placed2d, "%s.vertexUvTwo" % file_node, f=True)
    cmds.connectAttr("%s.vertexUvThree" % placed2d, "%s.vertexUvThree" % file_node, f=True)
    cmds.connectAttr("%s.vertexCameraOne" % placed2d, "%s.vertexCameraOne" % file_node, f=True)
    cmds.connectAttr("%s.outUV" % placed2d, "%s.uv" % file_node)
    cmds.connectAttr("%s.outUvFilterSize" % placed2d, "%s.uvFilterSize" % file_node)
    return file_node

  def setTexture(self, file_node, material):
    cmds.setAttr("%s.fileTextureName" % file_node, self.directory + "texture/" + material.texture, type="string")

  def setMaterial(self, mat_node, file_node, material):
    cmds.setAttr("%s.color" % mat_node, material.diffuse_color[0], material.diffuse_color[1], material.diffuse_color[2], type="double3")
    cmds.setAttr("%s.transparency" % mat_node, material.transparent, material.transparent, material.transparent, type="double3")
    cmds.setAttr("%s.ambientColor" % mat_node, material.ambient_color[0], material.ambient_color[1], material.ambient_color[2], type="double3")
    cmds.setAttr("%s.specularColor" % mat_node, material.specular_color[0], material.specular_color[1], material.specular_color[2], type="double3")
    cmds.setAttr("%s.eccentricity" % mat_node, material.specularity)
    cmds.setAttr("%s.specularRollOff" % mat_node, material.specularity)

    ext = os.path.splitext(material.texture)[1]
    if material.transparent > 0.0 and (ext == ".png" or ext == ".tga"):
      cmds.connectAttr("%s.outTransparency" % file_node, "%s.transparency" % mat_node)
