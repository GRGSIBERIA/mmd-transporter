#-*- encoding: utf-8

import maya.cmds
import maya.OpenMaya

import pymeshio
import pymeshio.pmx

class OutMesh:

  def __init__(self, mmdModel):
    self.mmdModel = mmdModel


  def _whileAll(self, transform, attrName):
    arr = []
    for cnt in range(maya.cmds.polyEvaluate(v=True)):
      e = maya.cmds.getAttr("%s.%s[%s]" % (transform, attrName, cnt))
      e[1] = 1.0 - e[1]
      arr.append(e)
    return arr


  def _initUVs(self, transform):
    return self._whileAll(transform, "uv")


  def _connectFaces(self, transform):
    faces = []
    for cnt in range(maya.cmds.polyEvaluate(f=True)):
      maya.cmds.select("%s.f[%s]" % (transform, cnt))
      maya.cmds.ConvertSelectionToUVs()
      uvs = maya.cmds.ls(sl=True, fl=True)
      elems = []
      for uv in uvs:
        elems.append(int(uv.split("[")[1][:-1]))
      faces.append(elems)

    maya.cmds.select(cl=True)
    print faces
    return faces


  def _initializeVertices(self, transform):
    uvs = self._initUVs(transform)
    faces = self._connectFaces(transform)
    # UVから参照している頂点を求めてリスト化する
    # 頂点から参照しているUV添字配列のリストが必要
    # これがないとskinPercentしたときに頂点指定だから困る


  def generate(self, transform):
    self._initializeVertices(transform)
