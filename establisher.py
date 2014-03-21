#-*- encoding: utf-8
import maya.cmds as cmds


class AxisLimitter:
  def __init__(self):
    pass

  def giveAxis(self, bone):
    if bone.enable_axis == 1:
      cmds.select(bone.maya_name)
      axis_joint = cmds.joint(r=True, p=bone.limit_axis)
      #cmds.joint(bone.maya_name, e=True, zso=True, oj="xyz", sao="yup")
      cmds.setAttr("%s.jointTypeY" % bone.maya_name, 0)
      cmds.setAttr("%s.jointTypeZ" % bone.maya_name, 0)
      cmds.setAttr("%s.ry" % bone.maya_name, lock=True)
      cmds.setAttr("%s.rz" % bone.maya_name, lock=True)
      cmds.setAttr("%s.drawStyle" % axis_joint, 2)
      cmds.delete(axis_joint)

  def giveLocal(self, bone):
    if bone.enable_local == 1:
      # 1. Z軸に対してジョイントを伸ばす（-zso -oj xyz -sao yup）
      # 2. X軸にジョイントを伸ばす
      # 3. Z軸のジョイントを削除する
      # 4. X軸に対してorientJointをかける（-zso -oj xyz）
      print "local: %s" % bone.enable_local
      cmds.select(bone.maya_name)
      z_axis = cmds.joint(r=True, p=bone.local_z, zso=True, oj="xyz", sao="yup", name="%s_local_z" % bone.maya_name)
      cmds.select(bone.maya_name)
      x_axis = cmds.joint(r=True, p=bone.local_x, name="%s_local_x" % bone.maya_name)
      
      #cmds.delete(z_axis)
      #cmds.select(x_axis)
      #cmds.joint(e=True, zso=True, oj="xyz", ch=True)
      #cmds.delete(x_axis)

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

  def giveAttr(self, bone_inst, bones):
    if bone_inst.is_establish_rotation == 1:
      self._createExpression(bone_inst, bones, "rotate")
    if bone_inst.is_establish_translate == 1:
      self._createExpression(bone_inst, bones, "translate")

  def _createExpression(self, bone_inst, bones, attr_type):
    parent_joint = bones[bone_inst.establish_parent]
    #pbuf = bones[bone_inst.parent_bone_name]
    #self._asyncOrientJointFromParent(bone_inst, pbuf)
    script = self._createScript(bone_inst, bones, attr_type, parent_joint)
    name = "establish_%s_for_%s_from_%s" % (attr_type, bone_inst.maya_name, parent_joint.maya_name)
    #cmds.expression(s=script, n=name)

  def _createScript(self, bone_inst, bones, attr_type, parent_joint):
    script = ""
    return script

# parent.worldSpaceRotate = parent.rotate + parent.orientJoint
# child.rotate = parent.worldSpaceRotate - child.orientJoint
#