#-*- encoding: utf-8
import sys
import os.path

import maya.OpenMaya
import maya.OpenMayaMPx
import maya.cmds

import meshgen

class MMDPoly(maya.OpenMayaMPx.MPxNode):
  widthHeight = maya.OpenMaya.MObject()
  outputMesh = maya.OpenMaya.MObject()
  mmdData = None

  def __init__(self):
    maya.OpenMayaMPx.MPxNode.__init__(self)

  def _setNormals(self, meshFS, mmdData, faceConnects):
    normalLength = len(mmdData.indices)
    faceInds = maya.OpenMaya.MIntArray(normalLength)
    normals = maya.OpenMaya.MVectorArray(normalLength)
    for i in range(normalLength):
        faceInds.set(i / 3, i)
        vtxInd = mmdData.indices[i]
        normal = mmdData.vertices[vtxInd].normal
        normals.set(maya.OpenMaya.MVector(normal.x, normal.y, -normal.z), i)
    meshFS.setFaceVertexNormals(normals, faceInds, faceConnects)

  def _createMesh(self, planeSize, outData, mmdData):
    meshGen = meshgen.MeshGenerator(mmdData)

    points = meshGen.CreatePoints()
    faceConnects = meshGen.CreateFaceConnects()
    faceCounts = meshGen.CreateFaceCounts()
    uArray, vArray = meshGen.CreateUVArray()

    meshFS = maya.OpenMaya.MFnMesh()
    newMesh = meshFS.create(points.length(), faceCounts.length(), points, faceCounts, faceConnects, uArray, vArray, outData)

    meshFS.assignUVs(faceCounts, faceConnects)

    self._setNormals(meshFS, mmdData, faceConnects)

    return newMesh

  def compute(self, plug, data):
    if plug == MMDPoly.outputMesh:
        dataHandle = data.inputValue(MMDPoly.widthHeight)
        size = dataHandle.asFloat()

        dataCreator = maya.OpenMaya.MFnMeshData()
        newOutputData = dataCreator.create()
        self._createMesh(size, newOutputData, MMDPoly.mmdData)

        outputHandle = data.outputValue(MMDPoly.outputMesh)
        outputHandle.setMObject(newOutputData)
        data.setClean(plug)
    else:
        return maya.OpenMaya.kUnknownParameter
