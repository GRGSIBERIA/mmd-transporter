#-*- encoding: utf-8

import maya.cmds
import maya.OpenMaya

class Mesh:
  
  def _initUVs(self):
    uvs = []
    maya.cmds.select(self.transform)
    for cnt in range(maya.cmds.polyEvaluate(uv=True)):
      uv = list(maya.cmds.getAttr("%s.uv[%s]" % (self.transform, cnt))[0])
      uv[1] = 1.0 - uv[1]
      uvs.append(uv)
    return uvs


  def _initUVToVertex(self, uvs):
    vtxs = []
    for i in range(len(uvs)):
      maya.cmds.select("%s.uv[%s]" % (self.transform, i))
      maya.cmds.ConvertSelectionToVertices()
      v = maya.cmds.ls(sl=True)
      if len(v) > 1:
        print v
      vtxs.append(int(v[0].split("[")[1][:-1]))
    return vtxs


  def _initVertices(self, uvToVertex):
    vtxs = []
    for i in range(len(uvToVertex)):
      vtx = maya.cmds.xform("%s.vtx[%s]" % (self.transform, uvToVertex[i]), a=True, t=True, q=True, ws=True)
      vtx[2] = -vtx[2]
      vtxs.append(vtx)
    return vtxs


  def _connectFaces(self):
    faces = []
    maya.cmds.select(self.transform)
    for cnt in range(maya.cmds.polyEvaluate(f=True)):
      maya.cmds.select("%s.f[%s]" % (self.transform, cnt))
      maya.cmds.ConvertSelectionToUVs()
      uvs = maya.cmds.ls(sl=True, fl=True)
      elems = []
      for uv in uvs:
        elems.append(int(uv.split("[")[1][:-1]))
      faces.append(elems)

    maya.cmds.select(cl=True)
    return faces


  def _initNormals(self, uvToVertex):
    normals = []
    for i in range(len(uvToVertex)):
      maya.cmds.select("%s.vtx[%s]" % (self.transform, uvToVertex[i]))
      result = maya.cmds.polyNormalPerVertex(q=True, xyz=True)
      result[2] = -result[2]
      normals.append(result[:3])
    return normals


  def _toVector(self, v):
    scriptUtil = maya.OpenMaya.MScriptUtil()
    scriptUtil.createFromDouble(v[0], v[1], v[2])
    ptr = scriptUtil.asDoublePtr()
    return maya.OpenMaya.MVector(ptr)


  def _checkBothSidesFromTriangle(self, vectors, n):
    v1 = vectors[1] - vectors[0]
    v2 = vectors[2] - vectors[0]
    v1.normalize()
    v2.normalize()
    cross = v1 ^ v2   # 外積を取って三角形の向きを見る
    normal = self._toVector(n)
    dotProduct = cross * normal   # 内積を取って法線の向きと同じか確かめる
    return dotProduct >= 0.0


  def _arrangeTriangleList(self):
    for i in range(len(self.faces)):
      triangle = self.faces[i]
      vectors = []
      for index in triangle:
        vectors.append(self._toVector(self.vertices[index]))

      normal = self.normals[triangle[0]]
      bothSideFlag = self._checkBothSidesFromTriangle(vectors, normal)
      if not (bothSideFlag):   # 逆向きだったら並べ替える
        tmp = triangle[1]
        triangle[1] = triangle[2]
        triangle[2] = tmp
      self.faces[i] = triangle  # なんか不安になる


  def _initializeMesh(self):
    self.uvs = self._initUVs()
    self.uvToVertex = self._initUVToVertex(self.uvs)
    self.vertices = self._initVertices(self.uvToVertex)
    self.faces = self._connectFaces()
    self.normals = self._initNormals(self.uvToVertex)
    self._arrangeTriangleList()


  def __init__(self, transform):
    self.transform = transform
    self._initializeMesh()