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

kNodeName = "MMD Transporter"
kNodeId = OM.MTypeId(0x3939)

def nodeCreator():
    pass

def nodeInitializer():
    pass

# プラグインの初期化
def initializePlugin(obj):
    plugin = MPx.MFnPlugin(obj)
    try:
        plugin.registerNode(kNodeName, kNodeId, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write('Failed to register node: %s' % (kNodeName))
        raise

# プラグインの解放
def uninitializePlugin(obj):
    plugin = MPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(kNodeId)
    except:
        sys.stderr.write('Failed to deregister node: %s' % (kNodeName))