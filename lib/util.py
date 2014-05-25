#-*- encoding: utf-8

import maya.cmds

def setJpName(objName, jpName):
  maya.cmds.addAttr(objName, dt="string", ln="jpName", h=False, k=False)
  maya.cmds.setAttr("%s.jpName" % objName, jpName, typ="string")

def getJpName(objName):
  return maya.cmds.getAttr("%s.jpName" % objName)

def setAtAttr(objName, attrName, attrType, message):
  maya.cmds.addAttr(objName, at=attrType, ln=attrName, h=False, k=False)
  maya.cmds.setAttr("%s.%s" % (objName, attrName))

def setDtAttr(objName, attrName, attrType, message):
  maya.cmds.addAttr(objName, dt=attrType, ln=attrName, h=False, k=False)
  maya.cmds.setAttr("%s.%s" % (objName, attrName))

def setString(objName, attrName, message):
  setDtAttr(objName, attrName, "string", message)

def setInteger(objName, attrName, number):
  setAtAttr(objName, attrName, "long", number)

def setBoolean(objName, attrName, value):
  setAtAttr(objName, attrName, "bool", value)

def getString(objName, attrName):
  return maya.cmds.getAttr("%s.%s" % (objName, attrName))

def getAttr(objName, attrName):
  return maya.cmds.getAttr("%s.%s" % (objName, attrName))