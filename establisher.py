#-*- encoding: utf-8
import maya.cmds as cmds

class LimitEstablisher:
  def __init__(self):
    pass

  def giveLimit(self, joint_name, bone_inst):
    self._disableAttr(joint_name, "scale")
    if bone_inst.enable_rotate == 0:
      self._disableAttr(joint_name, "rotate")
    if bone_inst.enable_translate == 0:
      self._disableAttr(joint_name, "translate")
    if bone_inst.enable_visibility == 0:
      cmds.setAttr("%s.drawStyle" % joint_name, 2)

  def _disableAttr(self, joint_name, attribute):
    for e in ["X", "Y", "Z"]:
      cmds.setAttr("%s.%s%s" % (joint_name, attribute, e), k=False)

class AttributeEstablisher:
  def __init__(self):
    pass

  def giveAttr(self, joint_name, bone_inst, bones):
    if bone_inst.is_establish_rotation == 1:
      self._createExpression(joint_name, bone_inst, bones, "rotate")
    if bone_inst.is_establish_translate == 1:
      self._createExpression(joint_name, bone_inst, bones, "translate")
    # 末端のボーンのOrientJointが原因でExpressionが破綻する

  def _createExpression(self, joint_name, bone_inst, bones, attr_type):
    parent_joint_name = bones[bone_inst.establish_parent].maya_name
    script = self._createScript(joint_name, bone_inst, bones, attr_type, parent_joint_name)
    name = "establish_%s_for_%s_from_%s" % (attr_type, joint_name, parent_joint_name)
    cmds.expression(s=script, n=name)

  def _createScript(self, joint_name, bone_inst, bones, attr_type, parent_joint_name):
    script = ""
    for attr in ["X", "Y", "Z"]:
      script += "%s.%s%s = %s.%s%s * %s;\n" % (joint_name, attr_type, attr, parent_joint_name, attr_type, attr, bone_inst.establish_power)
    return script