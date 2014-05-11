import sys
import maya.OpenMaya
import maya.OpenMayaMPx

class ToMaya:
  @classmethod
  def vector3(cls, v):
    return maya.OpenMaya.MFloatPoint(v.x, v.y, v.z)