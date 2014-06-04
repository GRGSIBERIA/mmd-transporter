#-*- encoding: utf-8
import sys
import os.path
import maya.OpenMayaMPx
import maya.cmds

import pymeshio.pmx
import pymeshio.pmx.writer
import util

import outmesh

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


  def _searchMotherGroup(self):
    selections = maya.cmds.ls(sl=True)
    if len(selections) <= 0:
      raise StandardError, "Do not select object."

    select = selections[0]
    mother = maya.cmds.listRelatives(select, p=True)[0]
    mmdFlag = util.getAttr(mother, "mmdModel")
    if not mmdFlag:
      raise StandardError, "Do not mmdModel Group"
    return (mother, select)


  def _createData(self, args):
    filePath = self._saveFileDialog()
    if filePath != None:
      mmdModel = pymeshio.pmx.Model()
      motherGroup, transform = self._searchMotherGroup()

      omesh = outmesh.OutMesh(mmdModel, transform)
      omesh.generate()
      

  def doIt(self, args):
    try:
      argData = maya.OpenMaya.MArgDatabase(self.syntax(), args)
    except:
      pass
    else:
      self._createData(argData)