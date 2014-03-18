#-*- encoding: utf-8
import hashlib
import maya.cmds as cmds

class Bone:
  def __init__(self, number, bone_name, maya_name, abs_pos, rel_pos, parent_bone_name):
    self.number = number
    self.bone_name = bone_name
    #self.maya_name = maya_name
    self.maya_name = "joint"
    self.abs_pos = abs_pos
    self.rel_pos = rel_pos
    self.parent_bone_name = parent_bone_name

class BoneImporter:
  def __init__(self):
    pass

  def importCSV(self, records):
    bones = {}
    cnt = 0
    root = None
    for rows in records:
      if rows[0] == "Bone":
        #bone_name = hashlib.sha1(rows[1]).hexdigest()
        #parent = hashlib.sha1(rows[13]).hexdigest()
        bone_name = rows[1]
        parent = rows[13]
        maya_name = "joint" #rows[1] # テーブルで英文字に変換
        apos = self._to_float3(rows, 5)
        rpos = self._to_float3(rows, 16)
        bones[bone_name] = Bone(cnt, bone_name, maya_name, apos, rpos, parent)
        if cnt == 1:    # 0番はたぶん操作中心ボーン
          root = bone_name
        cnt += 1
    return bones, root

  def _to_float3(self, rows, start):
    return [float(rows[start]), float(rows[start+1]), -float(rows[start+2])]

class BoneGenerator:
  def __init__(self):
    pass

  def generate(self, records):
    bones, root_name = BoneImporter().importCSV(records)
    bone_objs = {}
    for bname, bone in bones.items():
      cmds.select(d=True)
      bone_objs[bname] = cmds.joint(p=bone.abs_pos)

    for bname, bone in bones.items():
      parent = bone.parent_bone_name
      if parent != "":
        print [bname, parent, bone_objs[bname], bone_objs[parent]]
        cmds.connectJoint(bone_objs[bname], bone_objs[parent], pm=True)

    return bone_objs, bones, root_name