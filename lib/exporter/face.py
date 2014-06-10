#-*- encoding: utf-8

import maya.cmds
import maya.mel

class Face:

  def _getNumber(self, name):
    return int(name[:-1].split("[")[1])

  # 要はindicesを作っている
  def _createLinearFaceList(self):
    linearFace = []
    for i in range(len(self.material.materialNames)):
      materialName = self.material.orderToMaterial[i]
      faces = self.material.materialToFaces[materialName]
      for face in faces:
        maya.cmds.select(face)
        maya.mel.eval("PolySelectConvert 4")
        vtxs = maya.cmds.ls(sl=True, fl=True)
        for v in vtxs:
          linearFace.append(self._getNumber(v))
    return linearFace


  def __init__(self, mmdModel, material):
    self.mmdModel = mmdModel
    self.material = material
    self.linearFace = self._createLinearFaceList()  # 頂点番号を並べた面頂点リスト

    self.mmdModel.indices = self.linearFace