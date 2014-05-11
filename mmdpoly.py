import sys
import os.path

import maya.OpenMaya
import maya.OpenMayaMPx
import maya.cmds

import pymeshio.pmx.reader
import pymeshio.pmd.reader

class MMDPoly(maya.OpenMayaMPx.MPxNode):
    widthHeight = maya.OpenMaya.MObject()
    outputMesh = maya.OpenMaya.MObject()

    def __init__(self):
        maya.OpenMayaMPx.MPxNode.__init__(self)

    def _createMesh(self, planeSize, outData):
        numFaces = 1

        filterName = "PMD/PMX (*.pmd *pmx);;PMD (*.pmd);;PMX (*.pmx)"
        filePath = maya.cmds.fileDialog2(ds=2, cap="Selet PMD/PMX", ff=filterName, fm=1)[0]
        root, extType = os.path.splitext(filePath)
        extType = extType.lower()

        mmdData = None
        if extType == ".pmd":
            mmdData = pymeshio.pmd.reader.read_from_file(filePath)

        elif extType == ".pmx":
            mmdData = pymeshio.pmx.reader.read_from_file(filePath)

        points = maya.OpenMaya.MFloatPointArray()
        numVertices = len(mmdData.vertices)
        points.setLength(numVertices)
        for i in range(numVertices):
            mmdPoint = mmdData.vertices[i].position
            vtxPoint = maya.OpenMaya.MFloatPoint(mmdPoint.x, mmdPoint.y, mmdPoint.z)
            points.set(vtxPoint, i)

        faceConnects = maya.OpenMaya.MIntArray()
        numIndices = len(mmdData.indices)
        faceConnects.setLength(numIndices)
        for i in range(numIndices):
            faceConnects[i] = mmdData.indices[i]

        faceCounts = maya.OpenMaya.MIntArray()
        numFaces = numIndices / 3
        faceCounts.setLength(numFaces)
        for i in range(numFaces):
            faceCounts[i] = 3

        meshFS = maya.OpenMaya.MFnMesh()
        newMesh = meshFS.create(numVertices, numFaces, points, faceCounts, faceConnects, outData)
        return newMesh

    def compute(self, plug, data):
        if plug == MMDPoly.outputMesh:
            dataHandle = data.inputValue(MMDPoly.widthHeight)
            size = dataHandle.asFloat()

            dataCreator = maya.OpenMaya.MFnMeshData()
            newOutputData = dataCreator.create()
            self._createMesh(size, newOutputData)

            outputHandle = data.outputValue(MMDPoly.outputMesh)
            outputHandle.setMObject(newOutputData)
            data.setClean(plug)
        else:
            return maya.OpenMaya.kUnknownParameter