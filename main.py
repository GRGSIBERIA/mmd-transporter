#-*- encoding: utf-8
import sys
import maya.OpenMaya
import maya.OpenMayaMPx

from array_maker import *
from csv_importer import *


kPluginNodeName = 'simplePoly1'
kPluginNodeId = maya.OpenMaya.MTypeId(0x03939)


class simplePoly1(maya.OpenMayaMPx.MPxNode):
    widthHeight = maya.OpenMaya.MObject()
    outputMesh = maya.OpenMaya.MObject()

    def __init__(self):
        maya.OpenMayaMPx.MPxNode.__init__(self)

    def _createMesh(self, outData):
        maker = ArrayMaker()
        csv = CSVImporter("C:/")

        

        vtxs = []
        for vtx in csv.vertices:
            vtxs.append(maya.OpenMaya.MFloatPoint(vtx[0], vtx[1], -vtx[2]))
        numVertices = len(vtxs)

        points = maya.OpenMaya.MFloatPointArray()
        points.setLength(numVertices)
        for i in range(numVertices):
            points.set(vtxs[i], i)
        print "points: " + str(points.length())

        numConnects = len(csv.indices)
        numFaces = len(csv.indices) / 3

        faceConnects = maya.OpenMaya.MIntArray()
        faceConnects.setLength(numConnects)
        for i in range(numConnects):
            faceConnects[i] = csv.indices[i]
        print "faceConnects: " + str(faceConnects.length())

        faceCounts = maya.OpenMaya.MIntArray()
        faceCounts.setLength(numFaces)
        for i in range(numFaces):
            faceCounts[i] = 3
        print "faceCounts: " + str(faceCounts.length())

        meshFS = maya.OpenMaya.MFnMesh()
        newMesh = meshFS.create(points.length(), faceCounts.length(), points, faceCounts, faceConnects, outData)
        return newMesh

    def compute(self, plug, data):
        if plug == simplePoly1.outputMesh:
            dataHandle = data.inputValue(simplePoly1.widthHeight)
            size = dataHandle.asFloat()

            dataCreator = maya.OpenMaya.MFnMeshData()
            newOutputData = dataCreator.create()
            self._createMesh(newOutputData)

            outputHandle = data.outputValue(simplePoly1.outputMesh)
            outputHandle.setMObject(newOutputData)
            data.setClean(plug)
        else:
            return maya.OpenMaya.kUnknownParameter

def nodeCreator():
    return maya.OpenMayaMPx.asMPxPtr(simplePoly1())

def nodeInitializer():
    nAttr = maya.OpenMaya.MFnNumericAttribute()
    simplePoly1.widthHeight = nAttr.create('widthHeight', 'wh', maya.OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.setStorable(1)

    typedAttr = maya.OpenMaya.MFnTypedAttribute()
    simplePoly1.outputMesh = typedAttr.create('outputMesh', 'out', maya.OpenMaya.MFnData.kMesh)
    simplePoly1.addAttribute(simplePoly1.widthHeight)
    simplePoly1.addAttribute(simplePoly1.outputMesh)
    simplePoly1.attributeAffects(simplePoly1.widthHeight, simplePoly1.outputMesh)


def initializePlugin(mobject):
    mplugin = maya.OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(kPluginNodeName, kPluginNodeId, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write('Failed to register node: %s' % kPluginNodeName)
        raise

def uninitializePlugin(mobject):
    mplugin = maya.OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( kPluginNodeId )
    except:
        sys.stderr.write('Failed to deregister node: %s' % kPluginNodeName)
        raise