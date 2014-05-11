import sys
import os.path

import maya.OpenMaya
import maya.OpenMayaMPx
import maya.cmds

class MeshGenerator:
  def __init__(self, mmdData, ext):
    self.mmdData = mmdData
    self.extension = ext.lower()

  def CreatePoints(self):
    points = maya.OpenMaya.MFloatPointArray()
    numVertices = len(self.mmdData.vertices)
    points.setLength(numVertices)
    for i in range(numVertices):
      mmdPoint = self.mmdData.vertices[i].position
      vtxPoint = maya.OpenMaya.MFloatPoint(mmdPoint.x, mmdPoint.y, mmdPoint.z)
      points.set(vtxPoint, i)
    return points

  def CreateConnects(self):
    faceConnects = maya.OpenMaya.MIntArray()
    numIndices = len(self.mmdData.indices)
    faceConnects.setLength(numIndices)
    for i in range(numIndices):
      faceConnects[i] = self.mmdData.indices[i]
    return faceConnects

  def CreateCounts(self):
    faceCounts = maya.OpenMaya.MIntArray()
    numFaces = len(self.mmdData.indices) / 3
    faceCounts.setLength(numFaces)
    for i in range(numFaces):
      faceCounts[i] = 3
    return faceCounts