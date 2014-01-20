#-*- encoding: utf-8
import maya.OpenMaya
import maya.OpenMayaMPx

class ArrayMaker:
  def __init__(self):
    pass

  def MakePoints(self, array):
    points = maya.OpenMaya.MFloatPointArray()
    points.setLength(len(array))
    for i in range(len(array)):
      vtx = maya.OpenMaya.MFloatPoint(array[i][0], array[i][1], array[i][2])
      points.set(vtx, i)
    return points

  def MakeFaceConnects(self, array):
    connects = maya.OpenMaya.MIntArray()
    connects.setLength(len(array))
    for i in range(len(array)):
        connects[i] = array[i]
    return connects

  def MakeFaceCounts(self, array):
    counts = maya.OpenMaya.MIntArray()
    counts.setLength(len(array))
    for i in range(len(array)):
      counts.set(3, i)
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
      normals.set(vec, i)  # もしかするとこれはだめ？
    return normals