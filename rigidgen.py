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
    self.constPI = 180.0 / 3.141592653589793


  def _initializePose(self, rigidObj, rigid):
    util.setJpName(rigidObj, rigid.name)
    pos = rigid.shape_position
    rot = rigid.shape_rotation
    maya.cmds.move(pos.x, pos.y, -pos.z)
    maya.cmds.rotate(-rot.x * self.constPI, rot.y * self.constPI, rot.z * self.constPI)
    maya.cmds.scale(0.01, 0.01, 0.01)
    maya.cmds.makeIdentity(apply=True, s=1)
    #maya.cmds.setAttr("%s.v" % rigidObj, 0)
    shape = bullet.RigidBody.CreateRigidBody().executeCommandCB()[1]
    return shape


  def _initializeParams(self, shape, param):
    maya.cmds.setAttr("%s.mass" % shape, param.mass)
    maya.cmds.setAttr("%s.linearDamping" % shape, param.linear_damping)
    maya.cmds.setAttr("%s.friction" % shape, param.friction)
    maya.cmds.setAttr("%s.angularDamping" % shape, param.angular_damping)
    maya.cmds.setAttr("%s.restitution" % shape, param.restitution)


  def _initializeColider(self, shape, rigid):
    maya.cmds.setAttr("%s.autoFit" % shape, 0)
    shapeSize = rigid.shape_size
    if rigid.shape_type == 0:   # sphere
      maya.cmds.setAttr("%s.colliderShapeType" % shape, 2)
      maya.cmds.setAttr("%s.radius" % shape, shapeSize[0])
    elif rigid.shape_type == 1: # box
      maya.cmds.setAttr("%s.colliderShapeType" % shape, 1)
      maya.cmds.setAttr("%s.extentsX" % shape, shapeSize[0])
      maya.cmds.setAttr("%s.extentsY" % shape, shapeSize[1])
      maya.cmds.setAttr("%s.extentsZ" % shape, shapeSize[2])
    elif rigid.shape_type == 2: # capsule
      maya.cmds.setAttr("%s.colliderShapeType" % shape, 3)
      maya.cmds.setAttr("%s.radius" % shape, shapeSize[0])
      maya.cmds.setAttr("%s.length" % shape, shapeSize[1])


  def _parentConstraint(self, a, b):
    maya.cmds.select(a)
    maya.cmds.select(b, tgl=True)
    maya.cmds.parentConstraint(mo=True)


  def _constructConstraint(self, bones, rigidObj, shape, rigid, jointNames):
    parentJoint = ""
    if rigid.bone_index != -1:
      parentJoint = jointNames[rigid.bone_index]
    mode = rigid.mode

    if parentJoint != "":
      if mode == 0:   # ボーン追従
        maya.cmds.setAttr("%s.bodyType" % shape, 1)
        current = bones[rigid.bone_index]
        parentJoint = jointNames[current.parent_index]
        self._parentConstraint(parentJoint, rigidObj)
      elif mode == 1: # 物理演算
        self._parentConstraint(rigidObj, parentJoint)
      elif mode == 2: # 物理＋ボーン位置合わせ
        self._parentConstraint(rigidObj, parentJoint)


  def _settingCollision(self, shape, rigid):
    collisionGroup = 2**rigid.collision_group
    noCollisionGroup = -rigid.no_collision_group - 1
    maya.cmds.setAttr("%s.collisionFilterGroup" % shape, collisionGroup)
    maya.cmds.setAttr("%s.collisionFilterMask" % shape, noCollisionGroup)

  
  def _createRigidObjects(self, jointNames):
    rigids = self.mmdData.rigidbodies
    joints = self.mmdData.joints
    bones = self.mmdData.bones
    rigidObjects = []
    rigidShapes = []
    for i in range(len(rigids)):
      # rigidbodyをくっつけるためのオブジェクトを生成する
      rigidObj = maya.cmds.polyCube(name="rigid_" + self.nameDict[i])[0]
      shape = self._initializePose(rigidObj, rigids[i])
      self._initializeParams(shape, rigids[i].param)
      self._initializeColider(shape, rigids[i])
      self._constructConstraint(bones, rigidObj, shape, rigids[i], jointNames)
      self._settingCollision(shape, rigids[i])

      rigidObjects.append(rigidObj)
      rigidShapes.append(shape)
    return rigidObjects, rigidShapes


  def _convertCoordinate(self, value, limitType, axis):
    if limitType == "angular" and axis == "X":
      return  -value * self.constPI
    elif limitType == "linear" and axis == "Z":
      return -value

    if limitType == "angular":
      return value * self.constPI

    return value


  def _setJointLimitation(self, constraint, minVector, maxVector, limitType, axis, i):
    args = (constraint, limitType, axis)
    minValue = minVector[i] #self._convertCoordinate(minVector[i], limitType, axis)
    maxValue = maxVector[i] #self._convertCoordinate(maxVector[i], limitType, axis)

    if minVector[i] == 0.0 and maxVector[i] == 0.0:
      maya.cmds.setAttr("%s.%sConstraint%s" % args, 2)
    else:
      maya.cmds.setAttr("%s.%sConstraint%s" % args, 2)
      maya.cmds.setAttr("%s.%sConstraintMin%s" % args, minValue)
      maya.cmds.setAttr("%s.%sConstraintMax%s" % args, maxValue)


  def _setSpringLimitation(self, constraint, limitVector, limitType, axis, i):
    limitValue = limitVector[i] #self._convertCoordinate(limitVector[i], limitType, axis)
    maya.cmds.setAttr("%s.%sSpringStiffness%s" % (constraint, limitType, axis), limitValue)

  def _constraintJoint(self, joint, rigidShapes):
    ai = joint.rigidbody_index_a
    bi = joint.rigidbody_index_b
    maya.cmds.select(rigidShapes[ai])
    maya.cmds.select(rigidShapes[bi], tgl=True)
    constraint = bullet.RigidBodyConstraint.CreateRigidBodyConstraint().executeCommandCB()[0]
    maya.cmds.setAttr("%s.constraintType" % constraint, 5)

    axis = ["X", "Y", "Z"]
    for i in range(3):
      self._setJointLimitation(constraint, joint.translation_limit_min, joint.translation_limit_max, "linear", axis[i], i)
      self._setJointLimitation(constraint, joint.rotation_limit_min, joint.rotation_limit_max, "angular", axis[i], i)
      self._setSpringLimitation(constraint, joint.spring_constant_translation, "linear", axis[i], i)
      self._setSpringLimitation(constraint, joint.spring_constant_rotation, "angular", axis[i], i)


  def _createJoint(self, rigidShapes):
    joints = self.mmdData.joints
    for i in range(len(joints)):
      self._constraintJoint(joints[i], rigidShapes)


  def generate(self, jointNames):
    rigidObjects, rigidShapes = self._createRigidObjects(jointNames)
    #self._createJoint(rigidShapes)