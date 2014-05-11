#-*- encoding: utf-8
import sys
import os.path
import maya.OpenMayaMPx
import maya.cmds

import pymeshio.pmx.reader
import pymeshio.pmd.reader

import mmdpoly as mpoly
import meshgen
import matgen

class LoadMMD(maya.OpenMayaMPx.MPxCommand):
  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  def _getPath(self):
    filterName = "PMD/PMX (*.pmd *pmx);;PMD (*.pmd);;PMX (*.pmx)"
    path = maya.cmds.fileDialog2(ds=2, cap="Selet PMD/PMX", ff=filterName, fm=1)
    if path != None:
      return path[0]
    return None

  def _getExt(self, filePath):
    root, extType = os.path.splitext(filePath)
    return extType.lower()

  def _readData(self, filePath, extName):
    mmdData = None
    if extName == ".pmd":
      mmdData = pymeshio.pmd.reader.read_from_file(filePath)

    elif extName == ".pmx":
      mmdData = pymeshio.pmx.reader.read_from_file(filePath)
    return mmdData

  def doIt(self, args):
    filePath = self._getPath()
    if filePath != None:
      extName = self._getExt(filePath)
      mmdData = self._readData(filePath, extName)
      mpoly.MMDPoly.mmdData = mmdData

      # ポリゴンの生成
      meshName = meshgen.MeshGenerator.CreatePolyNodes()

      # マテリアルの生成
      genMaterial = matgen.MaterialGenerator(mmdData, filePath)
      shaderGroupNames = genMaterial.generate()