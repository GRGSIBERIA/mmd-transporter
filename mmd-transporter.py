#-*- encoding: utf-8
import sys
import maya.OpenMaya
import maya.OpenMayaMPx

import mmdpoly as mdp
import mmdcommand as cmd

kPluginNodeName = 'mmdPoly'
kPluginNodeId = maya.OpenMaya.MTypeId(0x03939)
kPluginCmdName = "loadmmd"

def nodeCreator():
    return maya.OpenMayaMPx.asMPxPtr(mdp.MMDPoly())

def createCommand():
    return maya.OpenMayaMPx.asMPxPtr(cmd.LoadMMD())

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
    mplugin = maya.OpenMayaMPx.MFnPlugin(mobject, "Eiichi Takebuchi", "1.0")
    mplugin.registerNode(kPluginNodeName, kPluginNodeId, nodeCreator, nodeInitializer)
    mplugin.registerCommand(kPluginCmdName, createCommand)

def uninitializePlugin(mobject):
    mplugin = maya.OpenMayaMPx.MFnPlugin(mobject)
    mplugin.deregisterNode(kPluginNodeId)
    mplugin.deregisterCommand(kPluginCmdName)
