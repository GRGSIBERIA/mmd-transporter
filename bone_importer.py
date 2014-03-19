#-*- encoding: utf-8
import hashlib
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
        bone_name = rows[1]
        parent = rows[13]
        i = cnt + 1
        maya_name = u"joint%s" % i #rows[1] # テーブルで英文字に変換
        apos = self._to_float3(rows, 5)
        rpos = self._to_float3(rows, 16)
        bones[bone_name] = Bone(cnt, bone_name, maya_name, apos, rpos, parent)
        cnt += 1
    return bones

  def _to_float3(self, rows, start):
    return [float(rows[start]), float(rows[start+1]), -float(rows[start+2])]

class BoneGenerator:
  def __init__(self):
    pass

  def generate(self, records):
    bones = BoneImporter().importCSV(records)
    bone_objs = {}
    for bname, bone in bones.items():
      cmds.select(d=True)
      bone_objs[bname] = cmds.joint(p=bone.abs_pos)

    for bname, bone in bones.items():
      parent = bone.parent_bone_name
      if parent != "":
        cmds.connectJoint(bone_objs[bname], bone_objs[parent], pm=True)

    return bone_objs, bones

  def searchRoot(self, bones):
    maybe_root = {}
    for bone_name, bone in bones.items():
      root = self._recursiveSearch(bone_name, bones)
      if maybe_root.has_key(root) == False:
        maybe_root[root] = 0
      maybe_root[root] += 1
      if len(maybe_root) > 5:
        break   # 親なしボーンはさすがに5個もない考え
    return max(maybe_root.items(), key=lambda x:x[1])[0]

  def _recursiveSearch(self, bone_name, bones):
    bone = bones[bone_name]
    parent = bone.parent_bone_name
    if parent == "":
      return bone_name
    return self._recursiveSearch(parent, bones)