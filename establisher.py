#-*- encoding: utf-8
import maya.cmds as cmds

class AxisLimitter:
  def __init__(self):
    pass

  def giveAxis(self, bone):
    if bone.enable_axis == 1:
      axis_joint = cmds.joint(r=True, p=bone.limit_axis)
      cmds.joint(bone.maya_name, e=True, zso=True, oj="xyz", sao="yup")
      cmds.delete(axis_joint)
      cmds.setAttr("%s.jointTypeY" % bone.maya_name, 0)
      cmds.setAttr("%s.jointTypeZ" % bone.maya_name, 0)
      cmds.setAttr("%s.ry" % bone.maya_name, lock=True)
      cmds.setAttr("%s.rz" % bone.maya_name, lock=True)

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
    script = self._createScript(bone_inst, bones, attr_type, parent_joint)
    name = "establish_%s_for_%s_from_%s" % (attr_type, bone_inst.maya_name, parent_joint.maya_name)
    cmds.expression(s=script, n=name)

  def _createScript(self, bone_inst, bones, attr_type, parent_joint):
    script = ""
    for attr in ["X", "Y", "Z"]:
      script += "%s.%s%s = %s.%s%s * %s;\n" % (bone_inst.maya_name, attr_type, attr, parent_joint.maya_name, attr_type, attr, bone_inst.establish_power)
    return script