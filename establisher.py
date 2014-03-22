#-*- encoding: utf-8
import maya.cmds as cmds


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
    if bone.is_establish_rotation == 1:
      #self._createExpression(bone, bones, "rotate")
      est_p = bones[bone.establish_parent]
      world_rotation = cmds.xform(est_p.maya_name, q=True, r=True, ws=True, ro=True)
      script  = "$%s_b = `xform -q -r -ws -ro %s`;\n" % (bone.maya_name, est_p.maya_name)
      script += "%s.rotateX = $%s_b[0] - %s;\n" % (bone.maya_name, bone.maya_name, world_rotation[0])
      script += "%s.rotateY = $%s_b[1] - %s;\n" % (bone.maya_name, bone.maya_name, world_rotation[1])
      script += "%s.rotateZ = $%s_b[2] - %s;\n" % (bone.maya_name, bone.maya_name, world_rotation[2])
      print script
      cmds.expression(s=script, n="establish_rotation_for_%s_%s" % (est_p.maya_name, bone.maya_name))
    if bone.is_establish_translate == 1:
      #self._createExpression(bone, bones, "translate")
      pass

  def _createExpression(self, bone, bones, attr_type):
    pass

  def _createScript(self, bone, bones, attr_type, parent_joint):
    script = ""
    

    return script

# parent.worldSpaceRotate = parent.rotate + parent.orientJoint
# child.rotate = parent.worldSpaceRotate - child.orientJoint
#