#-*- encoding: utf-8
import maya.cmds as cmds

from establisher import *

class Bone:
  def __init__(self, number, record, maya_name):
    self.number = number
    self.bone_name = record[1]
    self.maya_name = maya_name
    self.abs_pos = self._to_float3(record, 5)
    self.rel_pos = self._to_float3(record, 16)
    self.parent_bone_name = record[13]

    self.enable_rotate = int(record[8])
    self.enable_translate = int(record[9])
    self.enable_visibility = int(record[11])

    self.is_establish_rotation = int(record[20])
    self.is_establish_translate = int(record[21])
    self.establish_power = float(record[22])
    self.establish_parent = record[23]

    self.enable_axis = int(record[24])
    self.limit_axis = self._to_float3(record, 25)

    self.enable_local = int(record[28])
    self.local_x = self._to_float3(record, 29)
    self.local_z = self._to_float3(record, 32)

  def _to_float3(self, rows, start):
    return [float(rows[start]), float(rows[start+1]), -float(rows[start+2])]


class BoneImporter:
  def __init__(self):
    pass

  def importCSV(self, records):
    bones = {}
    cnt = 0
    for rows in records:
      if rows[0] == "Bone":
        i = cnt + 1
        bone_name = rows[1]
        maya_name = u"joint%s" % i #rows[1] # テーブルで英文字に変換
        bones[bone_name] = Bone(cnt, rows, maya_name)
        cnt += 1
    return bones


class BoneGenerator:
  def __init__(self):
    pass

  def generate(self, records):
    bones = BoneImporter().importCSV(records)
    bone_objs = {}
    for bname, bone in bones.items():
      cmds.select(d=True)
      joint_name = cmds.joint(p=bone.abs_pos)
      bone_objs[bname] = joint_name
      bone.maya_name = joint_name

    axis_limit = AxisLimitter()
    #limit_estab = LimitEstablisher()
    #attr_estab = AttributeEstablisher()

    for bname, bone in bones.items():
      parent_name = bone.parent_bone_name
      if parent_name != "":
        parent_joint = bones[parent_name]
        #axis_limit.giveLocal(parent_joint)
        #axis_limit.giveAxis(parent_joint)
        cmds.connectJoint(bone.maya_name, parent_joint.maya_name, pm=True)

    # joint orientの調整
    root_name = self._searchRoot(bones) # ルートボーンを探索する
    
    # ローカル座標チェック
    for bname, bone in bones.items():
      if bone.parent_bone_name == "":
        continue
      parent = bones[bone.parent_bone_name]
      cmds.select(parent.maya_name)
      if parent.local_x[0] > 0.0:
        cmds.joint(parent.maya_name, e=True, zso=True, oj="xyz", sao="yup")
      else:
        cmds.joint(parent.maya_name, e=True, zso=True, oj="xyz", sao="ydown")


    # Orient Jointをかけると今まで作ったボーン構造が破綻する
    #cmds.select(bone_objs[root_name])
    #cmds.joint(e=True, oj="xyz", secondaryAxisOrient="yup", ch=True, zso=True)

    # 移動，回転の非表示
    #for bname, bone in bones.items():
    #  limit_estab.giveLimit(bone)

    # 回転・移動付与
    #for bname, bone in bones.items():
    #  attr_estab.giveAttr(bone, bones)

    return bone_objs, bones, root_name

  def _searchRoot(self, bones):
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
