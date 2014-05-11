#-*- encoding: utf-8
import sys
import os.path

import maya.OpenMaya
import maya.OpenMayaMPx
import maya.cmds

import converter as cnv

class MeshGenerator:
  def __init__(self, mmdData):
    self.mmdData = mmdData

  def CreatePoints(self):
    points = maya.OpenMaya.MFloatPointArray()
    numVertices = len(self.mmdData.vertices)
    points.setLength(numVertices)
    for i in range(numVertices):
      vtxPoint = cnv.ToMaya.vector3(self.mmdData.vertices[i].position)
      points.set(vtxPoint, i)
    return points

  def CreateFaceConnects(self):
    faceConnects = maya.OpenMaya.MIntArray()
    numIndices = len(self.mmdData.indices)
    faceConnects.setLength(numIndices)
    for i in range(numIndices):
      faceConnects[i] = self.mmdData.indices[i]
    return faceConnects

  def CreateFaceCounts(self):
    faceCounts = maya.OpenMaya.MIntArray()
    numFaces = len(self.mmdData.indices) / 3
    faceCounts.setLength(numFaces)
    for i in range(numFaces):
      faceCounts[i] = 3
    return faceCounts

  def CreateUVArray(self):
    uArray = maya.OpenMaya.MFloatArray()
    vArray = maya.OpenMaya.MFloatArray()
    length = len(self.mmdData.vertices)
    uArray.setLength(length)
    vArray.setLength(length)
    for i in range(length):
      uv = self.mmdData.vertices[i].uv
      cnv.ToMaya.uv(uv, i, uArray, vArray)
    return uArray, vArray

  @classmethod
  def CreatePolyNodes(cls):
    poly = maya.cmds.createNode('transform')
    mesh = maya.cmds.createNode('mesh', parent=poly)
    maya.cmds.sets(mesh, add='initialShadingGroup')
    spoly = maya.cmds.createNode('mmdPoly')
    maya.cmds.connectAttr(spoly + '.outputMesh', mesh + '.inMesh')
    return mesh