#-*- encoding: utf-8

import maya.cmds
import maya.OpenMaya

class Mesh:
  
  def _initUVs(self):
    uvs = []
    maya.cmds.select(self.transform)
    for cnt in range(maya.cmds.polyEvaluate(v=True)):
      uv = list(maya.cmds.getAttr("%s.uv[%s]" % (self.transform, cnt))[0])
      uv[1] = 1.0 - uv[1]
      uvs.append(uv)
    return uvs


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


  def _initUVToVertex(self, uvs):
    vtxs = []
    for i in range(len(uvs)):
      maya.cmds.select("%s.uv[%s]" % (self.transform, i))
      maya.cmds.ConvertSelectionToVertices()
      v = maya.cmds.ls(sl=True)[0]
      vtxs.append(int(v.split("[")[1][:-1]))
    return vtxs


  def _initVertices(self, uvToVertex):
    vtxs = []
    for i in range(len(uvToVertex)):
      vtx = maya.cmds.xform("%s.vtx[%s]" % (self.transform, uvToVertex[i]), a=True, t=True, q=True, ws=True)
      vtx[2] = -vtx[2]
      vtxs.append(vtx)
    return vtxs


  def _initVertexToUVs(self):
    vtxToUVs = []
    maya.cmds.select(self.transform)
    for i in range(maya.cmds.polyEvaluate(v=True)):
      maya.cmds.select("%s.vtx[%s]" % (self.transform, i))
      maya.cmds.ConvertSelectionToUVs()
      uvs = maya.cmds.ls(sl=True, fl=True)
      vtxToUVs.append(uvs)
    return vtxToUVs


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


  def _checkBothSidesFromTriangle(self, vectors):
    v1 = (vectors[1] - vectors[0]).normal
    v2 = (vectors[2] - vectors[0]).normal
    cross = v1 ^ v2   # 外積を取って三角形の向きを見る
    noraml = self._toVector(self.normals[i])
    dotProduct = cross * normal   # 内積を取って法線の向きと同じか確かめる
    return dotProduct >= 0.0


  def _arrangeTriangleStrip(self):
    for i in range(len(self.faces)):
      triangle = self.faces[i]
      vectors = []
      for vertex in triangle:
        vectors.append(self._toVector(vertex))

      bothSideFlag = self._checkBothSidesFromTriangle(vectors)
      if not (bothSideFlag):   # 逆向きだったら並べ替える
        tmp = triangle[1]
        triangle[1] = triangle[2]
        triangle[2] = tmp
      self.faces[i] = triangle  # なんか不安になる


  def _initializeMesh(self):
    self.uvs = self._initUVs()
    self.faces = self._connectFaces()
    self.uvToVertex = self._initUVToVertex(self.uvs)
    self.vertices = self._initVertices(self.uvToVertex)
    self.vertexToUVs = self._initVertexToUVs()
    self.normals = self._initNormals(self.uvToVertex)
    self._arrangeTriangleStrip()
    

  def __init__(self, transform):
    self.transform = transform
    self._initializeMesh()