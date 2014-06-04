#-*- encoding: utf-8

import maya.cmds
import maya.OpenMaya

class Mesh:
  
  def _initUVs(self):
    uvs = []
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
      vtx = list(maya.cmds.getAttr("%s.vtx[%s]" % (self.transform, uvToVertex[i]))[0])
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


  def _initializeMesh(self):
    self.uvs = self._initUVs()
    self.faces = self._connectFaces()
    self.uvToVertex = self._initUVToVertex(self.uvs)
    self.vertices = self._initVertices(self.uvToVertex)
    self.vtxToUVs = self._initVertexToUVs()
    self.normals = self._initNormals(self.uvToVertex)


  def __init__(self, transform):
    self.transform = transform
    self._initializeMesh()