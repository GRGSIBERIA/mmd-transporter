#-*- encoding: utf-8

import maya.cmds
import maya.OpenMaya

import pymeshio.common
import pymeshio.pmx


class Vertex:


  def _createDeform(self, i):
    # テスト中
    return pymeshio.pmx.Bdef1(0)

  def _initVertices(self):
    vertices = []
    for i in range(len(self.mesh.uvs)):
      bv = self.mesh.vertices[i]
      buv = self.mesh.uvs[i]
      bn = self.mesh.normals[i]
      position = pymeshio.common.Vector3(bv[0], bv[1], bv[2])
      uv = pymeshio.common.Vector2(buv[0], buv[1])
      normal = pymeshio.common.Vector3(bn[0], bn[1], bn[2])
      deform = self._createDeform(i)
      vertex = pymeshio.pmx.Vertex(position, normal, uv, deform, 0) # deform, edge_factor
      vertices.append(vertex)
    return vertices


  def __init__(self, mmdModel, transform, mesh, bone):
    self.mmdModel = mmdModel
    self.transform = transform
    self.mesh = mesh
    self.bone = bone

    self.vertices = self._initVertices()
    self.mmdModel.vertices = self.vertices
