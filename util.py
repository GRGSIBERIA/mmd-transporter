#-*- encoding: utf-8

import maya.cmds

def setJpName(objName, jpName):
  maya.cmds.addAttr(objName, dt="string", ln="jpName", h=False, k=False)
  maya.cmds.setAttr("%s.jpName" % objName, jpName, typ="string")