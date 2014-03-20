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
