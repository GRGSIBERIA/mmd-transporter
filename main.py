#-*- encoding: utf-8
import sys
import maya.OpenMaya
import maya.OpenMayaMPx

from array_maker import *
from csv_importer import *


kPluginNodeName = 'transportedMMD1'
kPluginNodeId = maya.OpenMaya.MTypeId(0x03939)


class MMDTransporter(maya.OpenMayaMPx.MPxNode):
    widthHeight = maya.OpenMaya.MObject()
    outputMesh = maya.OpenMaya.MObject()

    def __init__(self):
        maya.OpenMayaMPx.MPxNode.__init__(self)

    def _createMesh(self, outData):
        maker = ArrayMaker()
        csv = CSVImporter("C:/")

        points = maker.MakePoints(csv.vertices)
        faceConnects = maker.MakeFaceConnects(csv.indices)
        faceCounts = maker.MakeFaceCounts(len(csv.indices) / 3)

        meshFS = maya.OpenMaya.MFnMesh()
        newMesh = meshFS.create(points.length(), faceCounts.length(), points, faceCounts, faceConnects, outData)
        return newMesh

    def compute(self, plug, data):
        if plug == MMDTransporter.outputMesh:
            dataHandle = data.inputValue(MMDTransporter.widthHeight)
            size = dataHandle.asFloat()

            dataCreator = maya.OpenMaya.MFnMeshData()
            newOutputData = dataCreator.create()
            self._createMesh(newOutputData)

            outputHandle = data.outputValue(MMDTransporter.outputMesh)
            outputHandle.setMObject(newOutputData)
            data.setClean(plug)
        else:
            return maya.OpenMaya.kUnknownParameter

def nodeCreator():
    return maya.OpenMayaMPx.asMPxPtr(MMDTransporter())

def nodeInitializer():
    nAttr = maya.OpenMaya.MFnNumericAttribute()
    MMDTransporter.widthHeight = nAttr.create('widthHeight', 'wh', maya.OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.setStorable(1)

    typedAttr = maya.OpenMaya.MFnTypedAttribute()
    MMDTransporter.outputMesh = typedAttr.create('outputMesh', 'out', maya.OpenMaya.MFnData.kMesh)
    MMDTransporter.addAttribute(MMDTransporter.widthHeight)
    MMDTransporter.addAttribute(MMDTransporter.outputMesh)
    MMDTransporter.attributeAffects(MMDTransporter.widthHeight, MMDTransporter.outputMesh)


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