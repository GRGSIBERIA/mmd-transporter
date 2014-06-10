#-*- encoding: utf-8
import sys
import io
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
import face

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


  def _saveMmdModel(self, mmdModel, filePath):
    f = io.open(filePath + "/test.pmx", "wb")
    pymeshio.pmx.writer.write(f, mmdModel)
    f.flush()
    f.close()

  def _constructBone(self, grp, mmdModel):
    estab = establish.Establish(grp.bone, grp.boneNames)
    local = axis.LocalAxis(grp.boneNames)
    fixed = axis.FixedAxis(grp.boneNames)
    return bone.Bone(mmdModel, grp.boneNames, estab, local, fixed)

  def _createData(self, args):
    filePath = self._saveFileDialog()
    if filePath != None:
      mmdModel = pymeshio.pmx.Model()
      grp = group.Group()

      boneInst = self._constructBone(grp, mmdModel)

      meshInst = mesh.Mesh(grp.transform)
      mat = material.Material(mmdModel, grp.transform, filePath)
      v = vertex.Vertex(mmdModel, grp.transform, meshInst, boneInst)
      f = face.Face(mmdModel, mat)

      # わかっていること
      # テクスチャの参照がおかしいことになっている

      # わからないこと
      # 面の表示がおかしいのは法線と三角形の順番じゃなかった

      #mmdModel.textures = []   # テクスチャにバグあり、直す必要がある
      for m in mmdModel.materials:
        m.texture_index = 0
        m.alpha = 1.0

      self._saveMmdModel(mmdModel, filePath)

  def doIt(self, args):
    try:
      argData = maya.OpenMaya.MArgDatabase(self.syntax(), args)
    except:
      pass
    else:
      self._createData(argData)