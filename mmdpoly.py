import sys
import os.path

#-*- encoding: utf-8
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

    def _createMesh(self, planeSize, outData):
        filterName = "PMD/PMX (*.pmd *pmx);;PMD (*.pmd);;PMX (*.pmx)"
        filePath = maya.cmds.fileDialog2(ds=2, cap="Selet PMD/PMX", ff=filterName, fm=1)[0]
        root, extType = os.path.splitext(filePath)
        extType = extType.lower()

        mmdData = None
        if extType == ".pmd":
            mmdData = pymeshio.pmd.reader.read_from_file(filePath)

        elif extType == ".pmx":
            mmdData = pymeshio.pmx.reader.read_from_file(filePath)

        meshGen = meshgen.MeshGenerator(mmdData, extType)

        points = meshGen.CreatePoints()
        faceConnects = meshGen.CreateFaceConnects()
        faceCounts = meshGen.CreateFaceCounts()
        uArray, vArray = meshGen.CreateUVArray()

        print type(uArray)
        print type(vArray)

        meshFS = maya.OpenMaya.MFnMesh()
        newMesh = meshFS.create(points.length(), faceCounts.length(), points, faceCounts, faceConnects, uArray, vArray, outData)

        meshFS.assignUVs(faceCounts, faceConnects)
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