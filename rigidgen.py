#-*- encoding: utf-8

import maya.cmds
import maya.app.mayabullet as bullet

class RigidBodyGenerator:

  def __init__(self, mmdData):
    self.mmdData = mmdData

  def _createRigidBodies(self):
    rigidbodies = self.mmdData.rigidbodies
    rigidNames = []   # 0...bulletRigidBody, 1...bulletRigidBodyShape
    for i in range(len(rigidbodies)):
      maya.cmds.select(d=True)
      rigidName = bullet.RigidBody.CreateRigidBody(True).executeCommandCB()
      

  def generate(self, jointNames):
    pass