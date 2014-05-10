#-*- encoding: utf-8
import maya.OpenMaya
import maya.OpenMayaMPx

class ArrayMaker:
  def __init__(self):
    pass

  def MakePoints(self, vertices):
    points = maya.OpenMaya.MFloatPointArray()
    points.setLength(len(vertices))
    for i in range(len(vertices)):
      vtx = maya.OpenMaya.MFloatPoint(vertices[i][0], vertices[i][1], -vertices[i][2])
      points.set(vtx, i)
    return points

  def MakeFaceConnects(self, indices):
    faceConnects = maya.OpenMaya.MIntArray()
    faceConnects.setLength(len(indices))
    for i in range(len(indices)):
        faceConnects[i] = indices[i]
    return faceConnects

  def MakeFaceCounts(self, triangle_count):
    counts = maya.OpenMaya.MIntArray()
    counts.setLength(triangle_count)
    for i in range(triangle_count):
      counts[i] = 3
    return counts

  def MakeIndices(self, vtx_count):
    indices = maya.OpenMaya.MIntArray()
    for i in range(vtx_count):
      indices.set(i, i)
    return indices

  def MakeNormals(self, array):
    normals = maya.OpenMaya.MVectorArray()
    normals.setLength(len(array))
    for i in range(len(array)):
      vec = maya.OpenMaya.MVector(array[i][0], array[i][1], array[i][2])
      normals[i] = vec
    return normals

  def MakeSingles(self, array):
    singles = maya.OpenMaya.MFloatArray()
    singles.setLength(len(array))
    for i in range(len(array)):
      singles[i] = array[i]
    return singles