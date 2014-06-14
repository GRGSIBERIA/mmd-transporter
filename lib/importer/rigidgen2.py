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


  def _getYXZRotation(self, rigid):
    rot = rigid.shape_rotation
    rot = maya.OpenMaya.MEulerRotation(-rot.x, rot.y, rot.z, 4) #kYXZ
    quat = rot.asQuaternion()
    return quat.asEulerRotation()


  def _createGroup(self, rigid):
    pCube = maya.cmds.polyCube()[0]

    pos = rigid.shape_position
    maya.cmds.setAttr("%s.translateX" % pCube,  pos.x)
    maya.cmds.setAttr("%s.translateY" % pCube,  pos.y)
    maya.cmds.setAttr("%s.translateZ" % pCube, -pos.z)
    
    rot = rigid.shape_rotation
    rot = maya.OpenMaya.MEulerRotation(-rot.x, rot.y, rot.z, 4) #kYXZ
    quat = rot.asQuaternion()
    rot = quat.asEulerRotation()
    maya.cmds.setAttr("%s.rotateOrder" % pCube, 4)  # kYXZ
    maya.cmds.setAttr("%s.rotateX" % pCube, rot.x * self.constPI)
    maya.cmds.setAttr("%s.rotateY" % pCube, rot.y * self.constPI)
    maya.cmds.setAttr("%s.rotateZ" % pCube, rot.z * self.constPI)

    maya.cmds.setAttr("%s.scaleX" % pCube, 0.0001)
    maya.cmds.setAttr("%s.scaleY" % pCube, 0.0001)
    maya.cmds.setAttr("%s.scaleZ" % pCube, 0.0001)
    maya.cmds.makeIdentity(apply=True, s=1)
    return pCube


  def _instantiateCollider(self, rigid, dictName):
    shapeGroup = self._createGroup(rigid)
    shapeGroup = maya.cmds.rename(shapeGroup, "shape_" + dictName)
    maya.cmds.select(shapeGroup)
    collider = bullet.RigidBody.CreateRigidBody().executeCommandCB()[1]
    collider = maya.cmds.rename(collider, "rigid_" + dictName)
    return collider, shapeGroup


  def _setColliderSize(self, collider, rigid):
    maya.cmds.setAttr("%s.autoFit" % collider, 0)
    colliderSize = rigid.shape_size
    if rigid.shape_type == 0:   # sphere
      maya.cmds.setAttr("%s.colliderShapeType" % collider, 2)
      maya.cmds.setAttr("%s.radius" % collider, colliderSize[0])
      util.setFloat(collider, "defaultRadius", colliderSize[0])
    elif rigid.shape_type == 1: # box
      maya.cmds.setAttr("%s.colliderShapeType" % collider, 1)
      maya.cmds.setAttr("%s.extentsX" % collider, colliderSize[0] * 2)
      maya.cmds.setAttr("%s.extentsY" % collider, colliderSize[1] * 2)
      maya.cmds.setAttr("%s.extentsZ" % collider, colliderSize[2] * 2)
      util.setFloat(collider, "defaultExtentsX", colliderSize[0] * 2)
      util.setFloat(collider, "defaultExtentsY", colliderSize[1] * 2)
      util.setFloat(collider, "defaultExtentsZ", colliderSize[2] * 2)
    elif rigid.shape_type == 2: # capsule
      maya.cmds.setAttr("%s.colliderShapeType" % collider, 3)
      maya.cmds.setAttr("%s.radius" % collider, colliderSize[0])
      maya.cmds.setAttr("%s.length" % collider, colliderSize[1] + colliderSize[0] * 2)
      util.setFloat(collider, "defaultRadius", colliderSize[0])
      util.setFloat(collider, "defaultLength", colliderSize[1] + colliderSize[0] * 2)


  def _setParameters(self, collider, param):
    maya.cmds.setAttr("%s.mass" % collider, param.mass)
    maya.cmds.setAttr("%s.linearDamping" % collider, param.linear_damping)
    maya.cmds.setAttr("%s.friction" % collider, param.friction)
    maya.cmds.setAttr("%s.angularDamping" % collider, param.angular_damping)
    maya.cmds.setAttr("%s.restitution" % collider, param.restitution)
    util.setFloat(collider, "defaultMass", param.mass)
    util.setFloat(collider, "defaultLinearDamping", param.linear_damping)
    util.setFloat(collider, "defaultFriction", param.friction)
    util.setFloat(collider, "defaultAngularDamping", param.angular_damping)
    util.setFloat(collider, "defaultRestitution", param.restitution)


  def _setRigidbodyType(self, collider, rigid):
    name = "%s.bodyType" % collider
    if rigid.mode == 0:
      maya.cmds.setAttr(name, 1)  # Kinematic
    elif rigid.mode == 1 or rigid.mode == 2:
      maya.cmds.setAttr(name, 2)  # Dynamic


  def _setCollisionFilter(self, collider, rigid):
    collisionGroup = 2**rigid.collision_group
    noCollisionGroup = (-rigid.no_collision_group - 1) ^ 0xFFFF
    maya.cmds.setAttr("%s.collisionFilterGroup" % collider, collisionGroup)
    maya.cmds.setAttr("%s.collisionFilterMask" % collider, noCollisionGroup)


  def _setConstraintCollider(self, colliderShape, rigid, jointNames):
    if rigid.bone_index != -1:
      targetJoint = jointNames[rigid.bone_index]

      if rigid.mode == 0: # ボーン追従
        maya.cmds.parentConstraint(targetJoint, colliderShape, mo=True)
      elif rigid.mode == 1 or rigid.mode == 2:  # 物理演算、位置合わせ
        maya.cmds.parentConstraint(colliderShape, targetJoint, mo=True)


  def _createRigidbodies(self, jointNames):
    rigids = self.mmdData.rigidbodies
    shapes = []
    colliders = []
    for i in range(len(rigids)):
      rigid = rigids[i]
      maya.cmds.select(d=True)

      collider, shape = self._instantiateCollider(rigid, self.nameDict[i])
      self._setColliderSize(collider, rigid)
      self._setParameters(collider, rigid.param)
      self._setRigidbodyType(collider, rigid)
      self._setCollisionFilter(collider, rigid)
      self._setConstraintCollider(shape, rigid, jointNames)
      

      shapes.append(shape)
      colliders.append(collider)
    return colliders, shapes


  def _instantiateConstraint(self, joint):
    ai = joint.rigidbody_index_a
    bi = joint.rigidbody_index_b
    maya.cmds.select(self.colliders[ai])
    maya.cmds.select(self.colliders[bi], tgl=True)
    constraint = bullet.RigidBodyConstraint.CreateRigidBodyConstraint().executeCommandCB()[0]
    shape = constraint.replace("Shape", "")
    maya.cmds.setAttr("%s.constraintType" % constraint, 5)
    name = "joint_%s_%s" % (self.colliders[ai], self.colliders[bi])
    constraint = maya.cmds.rename(constraint, name)
    shape = maya.cmds.rename(shape, "s" + name)
    return constraint, shape


  def _setJointLimitation(self):
    pass


  def _createConstraints(self, jointNames):
    constraints = []
    constraintShapes = []
    joints = self.mmdData.joints

    for i in range(len(joints)):
      joint = joints[i]
      constraint, shape = self._instantiateConstraint(joint)

      self._setJointLimitation()

      constraints.append(constraint)
      constraintShapes.append(shape)
    return constraints, constraintShapes


  def generate(self, jointNames):
    self.jointNames = jointNames
    self.colliders, self.colliderShapes = self._createRigidbodies(jointNames)
    self.constraints, self.constraintShapes = self._createConstraints(jointNames)
    return self.colliderShapes, self.constraintShapes

"""
メモ
剛体の重心位置は関連ボーンのところ？
"""