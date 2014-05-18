#-*- encoding: utf-8

import maya.cmds
import maya.app.mayabullet as bullet

import filemanager
import os.path
import util

class RigidBodyGenerator:

  def __init__(self, mmdData, filePath):
    self.mmdData = mmdData
    self.directory = os.path.dirname(filePath)
    self.nameDict, self.dictFlag = filemanager.openCSV(self.directory, "rigiddict.csv")


  def _createRigidBodies(self):
    rigidbodies = self.mmdData.rigidbodies
    rigidNames = []   # 0...bulletRigidBody, 1...bulletRigidBodyShape
    for i in range(len(rigidbodies)):
      maya.cmds.select(d=True)
      rigidName = bullet.RigidBody.CreateRigidBody(True).executeCommandCB()
      rigidName = maya.cmds.rename(rigidName, self.nameDict[i])
      util.setJpName(rigidName, rigidbodies[i].name)
      rigidNames.append(rigidName)
    return rigidNames


  def generate(self, jointNames):
    rigidNames = self._createRigidBodies(self)