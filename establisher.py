#-*- encoding: utf-8
import maya.cmds as cmds
import maya.mel as mel


class AxisLimitter:
  def __init__(self):
    pass

  def giveAxis(self, bone):
    if bone.enable_axis == 1:
      cmds.select(bone.maya_name)
      #makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1 -jointOrient;
      cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1, jointOrient=True)
      axis_joint = cmds.joint(r=True, p=bone.limit_axis, name="%s_axis" % bone.maya_name)
      cmds.joint(bone.maya_name, e=True, zso=True, oj="xyz")
      #cmds.setAttr("%s.jointTypeY" % bone.maya_name, 0)
      #cmds.setAttr("%s.jointTypeZ" % bone.maya_name, 0)
      #cmds.setAttr("%s.ry" % bone.maya_name, lock=True)
      #cmds.setAttr("%s.rz" % bone.maya_name, lock=True)
      #cmds.setAttr("%s.drawStyle" % axis_joint, 2)
      cmds.delete(axis_joint)

  def giveLocal(self, bone):
    if bone.enable_local == 1:
      # 1. Z軸に対してジョイントを伸ばす（-zso -oj xyz -sao yup）
      cmds.select(bone.maya_name)
      cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1, jointOrient=True)
      z_axis = cmds.joint(r=True, p=bone.local_z, name="%s_local_z" % bone.maya_name)
      cmds.select(bone.maya_name)
      cmds.joint(e=True, zso=True, oj="xyz", sao="yup")
      cmds.delete(z_axis)

      # 2. X軸にジョイントを伸ばす
      cmds.select(bone.maya_name)
      cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1, jointOrient=True)
      x_axis = cmds.joint(r=True, p=bone.local_x, name="%s_local_x" % bone.maya_name)
      cmds.select(bone.maya_name)
      cmds.joint(e=True, zso=True, oj="xyz")
      cmds.delete(x_axis)


class LimitEstablisher:
  def __init__(self):
    pass

  def giveLimit(self, bone_inst):
    self._disableAttr(bone_inst.maya_name, "scale")
    if bone_inst.enable_rotate == 0:
      self._disableAttr(bone_inst.maya_name, "rotate")
    if bone_inst.enable_translate == 0:
      self._disableAttr(bone_inst.maya_name, "translate")
    if bone_inst.enable_visibility == 0:
      cmds.setAttr("%s.drawStyle" % bone_inst.maya_name, 2)

  def _disableAttr(self, joint_name, attribute):
    for e in ["X", "Y", "Z"]:
      cmds.setAttr("%s.jointType%s" % (joint_name, e), 0)
      cmds.setAttr("%s.%s%s" % (joint_name, attribute, e), k=False)


class AttributeEstablisher:
  def __init__(self):
    pass

  def giveAttr(self, bone, bones):
    if bone.enable_establish_rotation == 1:
      parent_joint = bones[bone.establish_parent]
      cmds.select(parent_joint.maya_name)
      cmds.select(bone.maya_name, tgl=True)
      constraint = cmds.orientConstraint(mo=True)[0]
      multiply = cmds.createNode("multiplyDivide", n="%s_orientConstraint_multiplyDivide" % bone.maya_name)
      cmds.setAttr("%s.input2" % multiply, bone.establish_power, bone.establish_power, bone.establish_power, type="double3")
      cmds.connectAttr("%s.output" % multiply, "%s.rotate" % bone.maya_name, f=True)
      cmds.connectAttr("%s.constraintRotate" % constraint, "%s.input1" % multiply, f=True)
      # outputConstraint

    if bone.enable_establish_translate == 1:
      pass