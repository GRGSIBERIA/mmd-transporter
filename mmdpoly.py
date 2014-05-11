#-*- encoding: utf-8
import sys
import os.path

import maya.OpenMaya
import maya.OpenMayaMPx
import maya.cmds

import pymeshio.pmx.reader
import pymeshio.pmd.reader

import meshgen

class MMDPoly(maya.OpenMayaMPx.MPxNode):
  widthHeight = maya.OpenMaya.MObject()
  outputMesh = maya.OpenMaya.MObject()

  def __init__(self):
    maya.OpenMayaMPx.MPxNode.__init__(self)

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

  def _createMesh(self, planeSize, outData, mmdData, extName):
    meshGen = meshgen.MeshGenerator(mmdData, extName)

    points = meshGen.CreatePoints()
    faceConnects = meshGen.CreateFaceConnects()
    faceCounts = meshGen.CreateFaceCounts()
    uArray, vArray = meshGen.CreateUVArray()

    meshFS = maya.OpenMaya.MFnMesh()
    newMesh = meshFS.create(points.length(), faceCounts.length(), points, faceCounts, faceConnects, uArray, vArray, outData)

    meshFS.assignUVs(faceCounts, faceConnects)
    return newMesh

  def compute(self, plug, data):
    if plug == MMDPoly.outputMesh:
      filePath = self._getPath()
      if filePath != None:
        extName = self._getExt(filePath)
        mmdData = self._readData(filePath, extName)

        dataHandle = data.inputValue(MMDPoly.widthHeight)
        size = dataHandle.asFloat()

        dataCreator = maya.OpenMaya.MFnMeshData()
        newOutputData = dataCreator.create()
        self._createMesh(size, newOutputData, mmdData, extName)

        outputHandle = data.outputValue(MMDPoly.outputMesh)
        outputHandle.setMObject(newOutputData)
        data.setClean(plug)
    else:
      return maya.OpenMaya.kUnknownParameter