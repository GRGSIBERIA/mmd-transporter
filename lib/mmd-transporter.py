#-*- encoding: utf-8
import sys
import os
import maya.OpenMaya
import maya.OpenMayaMPx

import exporter.savemmd as svmmd
import importer.mmdpoly as mdp
import importer.loadmmd as cmd
import windowcmd

kPluginNodeName = 'mmdPoly'
kPluginNodeId = maya.OpenMaya.MTypeId(0x03939)


def nodeCreator():
    return maya.OpenMayaMPx.asMPxPtr(mdp.MMDPoly())


def createLoadMmdCommand():
    return maya.OpenMayaMPx.asMPxPtr(cmd.LoadMMD())


# blend shape
def createBSWindowCommand():
    return maya.OpenMayaMPx.asMPxPtr(windowcmd.MmdBlendShapeWindowCommand())


# rigidbody adjuster
def createRAWindowCommand():
    return maya.OpenMayaMPx.asMPxPtr(windowcmd.MmdRigidbodyAdjustWindowCommand())


def createSaveMmdCommand():
    return maya.OpenMayaMPx.asMPxPtr(svmmd.SaveMmd())


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
    mplugin = maya.OpenMayaMPx.MFnPlugin(mobject, "Eiichi Takebuchi(GRGSIBERIA)", "1.0")
    mplugin.registerNode(kPluginNodeName, kPluginNodeId, nodeCreator, nodeInitializer)
    mplugin.registerCommand("loadmmd", createLoadMmdCommand, cmd.LoadMMD.syntaxCreator)
    mplugin.registerCommand("savemmd", createSaveMmdCommand, svmmd.SaveMmd.syntaxCreator)
    mplugin.registerCommand("mmdbswindow", createBSWindowCommand)
    mplugin.registerCommand("mmdrawindow", createRAWindowCommand)


def uninitializePlugin(mobject):
    mplugin = maya.OpenMayaMPx.MFnPlugin(mobject)
    mplugin.deregisterNode(kPluginNodeId)
    mplugin.deregisterCommand("loadmmd")
    mplugin.deregisterCommand("mmdbswindow")
    mplugin.deregisterCommand("mmdrawindow")
    mplugin.deregisterCommand("savemmd")