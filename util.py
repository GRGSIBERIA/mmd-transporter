#-*- encoding: utf-8

import maya.cmds

def setJpName(objName, jpName):
  maya.cmds.addAttr(objName, dt="string", ln="jpName", h=False, k=False)
  maya.cmds.setAttr("%s.jpName" % objName, jpName, typ="string")

def getJpName(objName):
  return maya.cmds.getAttr("%s.jpName" % objName)

def setString(objName, attrName, message):
  maya.cmds.addAttr(objName, dt="string", ln=attrName, h=False, k=False)
  maya.cmds.setAttr("%s.%s" % (objName, attrName), message, typ="string")

def getString(objName, attrName):
  return maya.cmds.getAttr("%s.%s" % (objName, attrName))