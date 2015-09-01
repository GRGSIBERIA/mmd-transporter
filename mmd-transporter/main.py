#-*- encoding: utf-8
# Mayaを起動時に以下のコードを実行する
# import maya.cmds as cmds
# try: cmds.commandPort(name="127.0.0.1:6000", close=True, echoOutput=True)
# except: pass
# cmds.commandPort(name="127.0.0.1:6000", echoOutput=True)
# 実行したいコードを選択して，ToMayaでMayaに実行コードを転送できる

import sys
import maya.cmds
import maya.OpenMaya as OM
import maya.OpenMayaMPx as MPx;

import loadmmd
import savemmd

kNodeName = "MMD Transporter"
kNodeId = OM.MTypeId(0x3939)


def loadmmdCreator():
    return MPx.asMPxPtr(loadmmd.LoadMMD())

def savemmdCreator():
    return MPx.asMPxPtr(savemmd.SaveMMD())


def commandRegister(commandName, nodeCreatorFunc):
    plugin = MPx.MFnPlugin(obj)
    try:
        plugin.registerCommand(commandName, nodeCreatorFunc)
    except:
        sys.stderr.write('Failed to register command: %s' % (commandName))
        raise

def commandDeregister(commandName):
    plugin = MPx.MFnPlugin(obj)
    try:
        plugin.deregisterCommand(commandName)
    except:
        sys.stderr.write('Failed to register command: %s' % (commandName))
        raise


# プラグインの初期化
def initializePlugin(obj):
    commandRegister("loadmmd", loadmmdCreator)
    commandRegister("savemmd", savemmdCreator)

# プラグインの解放
def uninitializePlugin(obj):
    commandDeregister("loadmmd")
    commandDeregister("savemmd")