#-*- encoding: utf-8
import sys
import os.path
import maya.OpenMayaMPx
import maya.cmds

import pymeshio.pmx
import pymeshio.pmx.writer
import util

import group
import vertex
import mesh
import material
import establish
import axis
import bone

class SaveMmd(maya.OpenMayaMPx.MPxCommand):

  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)


  @classmethod
  def syntaxCreator(cls):
    syntax = maya.OpenMaya.MSyntax()
    return syntax


  def _saveFileDialog(self):
    path = maya.cmds.fileDialog2(ds=2, cap="Select Saving Directory", fm=3)
    if path != None:
      return path[0]
    return None


  def _createData(self, args):
    filePath = self._saveFileDialog()
    if filePath != None:
      mmdModel = pymeshio.pmx.Model()
      grp = group.Group()

      mat = material.Material(mmdModel, grp.transform, filePath)

      #meshInst = mesh.Mesh(transform)
      #v = vertex.Vertex(mmdModel, transform, meshInst)

      estab = establish.Establish(grp.bone, grp.boneNames)
      local = axis.LocalAxis(grp.boneNames)
      fixed = axis.FixedAxis(grp.boneNames)
      bn = bone.Bone(grp.boneNames, estab, local, fixed)

  def doIt(self, args):
    try:
      argData = maya.OpenMaya.MArgDatabase(self.syntax(), args)
    except:
      pass
    else:
      self._createData(argData)