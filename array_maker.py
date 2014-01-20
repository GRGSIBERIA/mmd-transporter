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
      points.set(vtx ,i)
    return points

  def MakeFaceConnects(self, array):
    connects = maya.OpenMaya.MIntArray()
    connects.setLength(len(array)*3)
    for i in range(len(array)):
      for j in range(3):
        connects[i*3+j] = array[i*3+j]
    return connects

  def MakeFaceCounts(self, array):
    counts = maya.OpenMaya.MIntArray()
    counts.setLength(len(array))
    for i in range(len(array)):
      counts.set(i, 3)
    return counts