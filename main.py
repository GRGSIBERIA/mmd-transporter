#-*- encoding: utf-8
import sys
import maya.OpenMaya
import maya.OpenMayaMPx

kPluginNodeName = 'simplePoly1'
kPluginNodeId = maya.OpenMaya.MTypeId(0x87007)

class simplePoly1(maya.OpenMayaMPx.MPxNode):
    widthHeight = maya.OpenMaya.MObject()
    outputMesh = maya.OpenMaya.MObject()

    def __init__(self):
        maya.OpenMayaMPx.MPxNode.__init__(self)

    def _createMesh(self, planeSize, outData):
        numFaces = 1

        vtxs = []
        vtxs.append(maya.OpenMaya.MFloatPoint(planeSize, 0.0, planeSize))
        vtxs.append(maya.OpenMaya.MFloatPoint(planeSize, 0.0, -planeSize))
        vtxs.append(maya.OpenMaya.MFloatPoint(-planeSize, 0.0, -planeSize))
        vtxs.append(maya.OpenMaya.MFloatPoint(-planeSize, 0.0,  planeSize))
        numVertices = len(vtxs)

        points = maya.OpenMaya.MFloatPointArray()
        points.setLength(numVertices)
        for i in range(numVertices):
            points.set(vtxs[i], i)

        faceConnects = maya.OpenMaya.MIntArray()
        faceConnects.setLength(4)
        faceConnects[0] = 1
        faceConnects[1] = 2
        faceConnects[2] = 3
        faceConnects[3] = 0

        faceCounts = maya.OpenMaya.MIntArray()
        faceCounts.setLength(numFaces)
        faceCounts.set(4, 0)

        meshFS = maya.OpenMaya.MFnMesh()
        newMesh = meshFS.create(numVertices, numFaces, points, faceCounts, faceConnects, outData)
        return newMesh

    def compute(self, plug, data):
        if plug == simplePoly1.outputMesh:
            dataHandle = data.inputValue(simplePoly1.widthHeight)
            size = dataHandle.asFloat()

            dataCreator = maya.OpenMaya.MFnMeshData()
            newOutputData = dataCreator.create()
            self._createMesh(size, newOutputData)

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