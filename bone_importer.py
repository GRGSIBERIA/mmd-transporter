#-*- encoding: utf-8
import maya.cmds as cmds

class Bone:
  def __init__(self, number, bone_name, maya_name, abs_pos, rel_pos, parent_bone_name):
    self.number = number
    self.bone_name = bone_name
    self.maya_name = maya_name
    self.abs_pos = abs_pos
    self.rel_pos = rel_pos
    self.parent_bone_name = parent_bone_name

class BoneImporter:
  def __init__(self):
    pass

  def importCSV(self, records):
    bones = {}
    cnt = 0
    for rows in records:
      if rows[0] == "Bone":
        bone_name = rows[1] # テーブルで英文字に変換
        apos = self._to_float3(rows, 5)
        rpos = self._to_float3(rows, 16)
        bones Bone(cnt, rows[1], bone_name, apos, rpos, rows[13])
        cnt += 1
    return bones

  def _to_float3(self, rows, start):
    return [float(rows[start]), float(rows[start+1]), float(rows[start+2])]

class BoneGenerator:
  def __init__(self):
    pass

  def generate(self, records):
    bones = BoneImporter().importCSV(records)
    bone_objs = {}
    for bname, bone in bones.items():
      cmds.select(d=True)
      bone_objs[bname] = cmds.joint(p=bone.abs_pos, name=bone.maya_name)

    for bname, bone in bones.items():
      parent = bone_objs[bone.parent_bone_name]
      cmds.connectJoint(bone_objs[bname], parent, pm=True)

    return bone_objs