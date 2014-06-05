#-*- encoding: utf-8

import maya.cmds
import maya.OpenMaya

import pymeshio
import pymeshio.pmx

import mesh

class Vertex:

  def __init__(self, mmdModel, transform, mesh):
    self.mmdModel = mmdModel
    self.transform = transform
    self.mesh = mesh


  def _initVertices(self):
    for i in range(len(self.mesh.uvs)):
      bv = self.mesh.vertices[i]
      buv = self.mesh.uvs[i]
      bn = self.mesh.normals[i]
      position = pymeshio.Vector3(bv[0], bv[1], bv[2])
      uv = pymeshio.Vector2(buv[0], buv[1])
      normal = pymeshio.Vector3(bn[0], bn[1], bn[2])
      vertex = pymeshio.pmx.Vertex(position, uv, normal, None, 0) # deform, edge_factor
      self.mmdModel.vertices.append(vertex)


  def generate(self):
    self._initVertices()