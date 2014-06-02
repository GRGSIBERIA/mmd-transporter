#-*- encoding: utf-8

import maya.cmds
import maya.app.mayabullet as bullet
import maya.OpenMaya

import os.path
import util


class RigidBodyGenerator:

  def __init__(self, mmdData, filePath, rigiddict):
    self.mmdData = mmdData
    self.directory = os.path.dirname(filePath)
    #self.nameDict, self.dictFlag = filemanager.openCSV(self.directory, "rigiddict.csv")
    self.nameDict = rigiddict
    self.dictFlag = True
    self.constPI = 180.0 / 3.141592653589793


  def _createPostureCube(self, rigid):
    pCube = maya.cmds.polyCube()[0]

    pos = rigid.shape_position
    maya.cmds.setAttr("%s.translateX" % pCube,  pos.x)
    maya.cmds.setAttr("%s.translateY" % pCube,  pos.y)
    maya.cmds.setAttr("%s.translateZ" % pCube, -pos.z)
    
    rot = rigid.shape_rotation
    rot = maya.OpenMaya.MEulerRotation(-rot.x, rot.y, rot.z, 4) #kYXZ
    quat = rot.asQuaternion()
    rot = quat.asEulerRotation()
    maya.cmds.setAttr("%s.rotateX" % pCube, rot.x * self.constPI)
    maya.cmds.setAttr("%s.rotateY" % pCube, rot.y * self.constPI)
    maya.cmds.setAttr("%s.rotateZ" % pCube, rot.z * self.constPI)

    maya.cmds.setAttr("%s.scaleX" % pCube, 0.0001)
    maya.cmds.setAttr("%s.scaleY" % pCube, 0.0001)
    maya.cmds.setAttr("%s.scaleZ" % pCube, 0.0001)
    maya.cmds.makeIdentity(apply=True, s=1)
    return pCube


  def _setColliderSize(self, shape, rigid):
    maya.cmds.setAttr("%s.autoFit" % shape, 0)
    shapeSize = rigid.shape_size
    if rigid.shape_type == 0:   # sphere
      maya.cmds.setAttr("%s.colliderShapeType" % shape, 2)
      maya.cmds.setAttr("%s.radius" % shape, shapeSize[0])
      util.setFloat(shape, "defaultRadius", shapeSize[0])
    elif rigid.shape_type == 1: # box
      maya.cmds.setAttr("%s.colliderShapeType" % shape, 1)
      maya.cmds.setAttr("%s.extentsX" % shape, shapeSize[0] * 2)
      maya.cmds.setAttr("%s.extentsY" % shape, shapeSize[1] * 2)
      maya.cmds.setAttr("%s.extentsZ" % shape, shapeSize[2] * 2)
      util.setFloat(shape, "defaultExtentsX", shapeSize[0] * 2)
      util.setFloat(shape, "defaultExtentsY", shapeSize[1] * 2)
      util.setFloat(shape, "defaultExtentsZ", shapeSize[2] * 2)
    elif rigid.shape_type == 2: # capsule
      maya.cmds.setAttr("%s.colliderShapeType" % shape, 3)
      maya.cmds.setAttr("%s.radius" % shape, shapeSize[0])
      maya.cmds.setAttr("%s.length" % shape, shapeSize[1] + shapeSize[0] * 2)
      util.setFloat(shape, "defaultRadius", shapeSize[0])
      util.setFloat(shape, "defaultLength", shapeSize[1] + shapeSize[0] * 2)


  def _setParams(self, shape, param):
    maya.cmds.setAttr("%s.mass" % shape, param.mass)
    maya.cmds.setAttr("%s.linearDamping" % shape, param.linear_damping)
    maya.cmds.setAttr("%s.friction" % shape, param.friction)
    maya.cmds.setAttr("%s.angularDamping" % shape, param.angular_damping)
    maya.cmds.setAttr("%s.restitution" % shape, param.restitution)
    util.setFloat(shape, "defaultMass", param.mass)
    util.setFloat(shape, "defaultLinearDamping", param.linear_damping)
    util.setFloat(shape, "defaultFriction", param.friction)
    util.setFloat(shape, "defaultAngularDamping", param.angular_damping)
    util.setFloat(shape, "defaultRestitution", param.restitution)


  def _parentConstraint(self, a, b):
    maya.cmds.select(a)
    maya.cmds.select(b, tgl=True)
    maya.cmds.parentConstraint(mo=True)


  def _constraintRigidbody(self, shape, pCube, rigid, jointNames):
    targetJoint = ""
    if rigid.bone_index >= 0 and len(jointNames) > rigid.bone_index:
      targetJoint = jointNames[rigid.bone_index]

    if targetJoint != "":
      if rigid.mode == 0:   # ボーン追従
        maya.cmds.setAttr("%s.bodyType" % shape, 1)
        maya.cmds.parentConstraint(targetJoint, pCube, mo=True)

      elif rigid.mode == 1: # 物理演算
        maya.cmds.setAttr("%s.bodyType" % shape, 2)
        #maya.cmds.parentConstraint(pCube, targetJoint, mo=True)
        maya.cmds.pointConstraint(targetJoint, pCube, mo=True)
        maya.cmds.orientConstraint(pCube, targetJoint, mo=True)

      elif rigid.mode == 2: # 位置合わせ
        maya.cmds.setAttr("%s.bodyType" % shape, 2)
        maya.cmds.pointConstraint(targetJoint, pCube, mo=True)
        maya.cmds.orientConstraint(pCube, targetJoint, mo=True)


  def _setCollisionFilter(self, shape, rigid):
    collisionGroup = 2**rigid.collision_group
    noCollisionGroup = (-rigid.no_collision_group - 1) ^ 0xFFFF
    maya.cmds.setAttr("%s.collisionFilterGroup" % shape, collisionGroup)
    maya.cmds.setAttr("%s.collisionFilterMask" % shape, noCollisionGroup)


  def _createRigidbodies(self, jointNames):
    rigids = self.mmdData.rigidbodies
    shapes = []
    for i in range(len(rigids)):
      rigid = rigids[i]
      maya.cmds.select(d=True)

      pCube = self._createPostureCube(rigid)
      pCube = maya.cmds.rename(pCube, "rcube_" + self.nameDict[i])
      maya.cmds.select(pCube)
      shape = bullet.RigidBody.CreateRigidBody().executeCommandCB()[1]
      shape = maya.cmds.rename(shape, "rigid_" + self.nameDict[i])
      util.setJpName(shape, rigid.name)

      self._setColliderSize(shape, rigid)
      self._setParams(shape, rigid.param)
      self._constraintRigidbody(shape, pCube, rigid, jointNames)
      self._setCollisionFilter(shape, rigid)
      shapes.append(shape)
    return shapes


  def _instantiateJoint(self, joint, shapes):
    ai = joint.rigidbody_index_a
    bi = joint.rigidbody_index_b
    maya.cmds.select(shapes[ai])
    maya.cmds.select(shapes[bi], tgl=True)
    constraint = bullet.RigidBodyConstraint.CreateRigidBodyConstraint().executeCommandCB()[0]
    maya.cmds.setAttr("%s.constraintType" % constraint, 5)
    constraint = maya.cmds.rename(constraint, "joint_%s_%s" % (shapes[ai], shapes[bi]))
    return constraint


  def _constraintJointWithRigidbody(self, constraint, joint, jointNames):
    ai = joint.rigidbody_index_b  # bが正解
    bi = self.mmdData.rigidbodies[ai].bone_index
    if bi >= 0 and bi < len(jointNames):
      parentBoneName = jointNames[bi]
      try:
        maya.cmds.pointConstraint(parentBoneName, constraint)
      except:
        print "Failed point constraint for joint solver: %s" % joint.name


  def _setJointLimitation(self, constraint, minVector, maxVector, limitType, axis, i):
    args = (constraint, limitType, axis)
    minValue = minVector[i]
    maxValue = maxVector[i]

    if minVector[i] > maxVector[i]:
      maya.cmds.setAttr("%s.%sConstraint%s" % args, 0)
    if minVector[i] == 0.0 and maxVector[i] == 0.0:
      maya.cmds.setAttr("%s.%sConstraint%s" % args, 1)
    else:
      maya.cmds.setAttr("%s.%sConstraint%s" % args, 2)
      maya.cmds.setAttr("%s.%sConstraintMin%s" % args, minValue)
      maya.cmds.setAttr("%s.%sConstraintMax%s" % args, maxValue)


  def _setSpringLimitation(self, constraint, limitVector, limitType, axis, i):
    limitValue = limitVector[i] #self._convertCoordinate(limitVector[i], limitType, axis)
    args = (constraint, limitType, axis)
    if limitValue > 0.0 or limitValue < 0.0:
      maya.cmds.setAttr("%s.%sSpringEnabled%s" % args, 1)
    maya.cmds.setAttr("%s.%sSpringStiffness%s" % args, limitValue)


  def _createJoints(self, shapes, jointNames):
    joints = self.mmdData.joints
    constraintNames = []
    solverNames = []
    for i in range(len(joints)):
      joint = joints[i]
      constraint = self._instantiateJoint(joint, shapes)
      try:
        solverName = maya.cmds.rename(u"bulletRigidBodyConstraint1", "solver_%s" % self.nameDict[i])
        self._constraintJointWithRigidbody(solverName, joint, jointNames)
        solverNames.append(solverName)
      except:
        print "Failed rename joint solver: %s" % joint.name

      axis = ["X", "Y", "Z"]
      for i in range(3):
        self._setJointLimitation(constraint, joint.translation_limit_min, joint.translation_limit_max, "linear", axis[i], i)
        self._setJointLimitation(constraint, joint.rotation_limit_min, joint.rotation_limit_max, "angular", axis[i], i)
        self._setSpringLimitation(constraint, joint.spring_constant_translation, "linear", axis[i], i)
        self._setSpringLimitation(constraint, joint.spring_constant_rotation, "angular", axis[i], i)
      
      constraintNames.append(constraint)

    return solverNames


  def generate(self, jointNames):
    rigidShapes = self._createRigidbodies(jointNames)
    constraintNames = self._createJoints(rigidShapes, jointNames)
    return rigidShapes, constraintNames

