import sys
import maya.OpenMaya
import maya.OpenMayaMPx

import mmdpoly as mdp

kPluginNodeName = 'mmdPoly'
kPluginNodeId = maya.OpenMaya.MTypeId(0x03939)



def nodeCreator():
    return maya.OpenMayaMPx.asMPxPtr(mdp.MMDPoly())

def nodeInitializer():
    nAttr = maya.OpenMaya.MFnNumericAttribute()
    mdp.MMDPoly.widthHeight = nAttr.create('widthHeight', 'wh', maya.OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.setStorable(1)

    typedAttr = maya.OpenMaya.MFnTypedAttribute()
    mdp.MMDPoly.outputMesh = typedAttr.create('outputMesh', 'out', maya.OpenMaya.MFnData.kMesh)
    mdp.MMDPoly.addAttribute(mdp.MMDPoly.widthHeight)
    mdp.MMDPoly.addAttribute(mdp.MMDPoly.outputMesh)
    mdp.MMDPoly.attributeAffects(mdp.MMDPoly.widthHeight, mdp.MMDPoly.outputMesh)


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