#-*- encoding: utf-8
import maya.cmds as cmds

class FaceMaterialGenerator:
  def __init__(self):
    pass

  def generate(self, records, model, shader_groups):
    cnt = 0
    mat_dict = {}

    for mat_name in shader_groups.keys():
      mat_dict[mat_name] = [] # 配列の初期化

    for row in records:
      if row[0] == "Face":
        mat_name = row[1]
        mat_dict[mat_name].append(cnt)  # カウントを入れていく
        cnt += 1

    for mat_name, counts in mat_dict.items():
      start = counts[0]
      end = counts[len(counts)-1]
      sg = shader_groups[mat_name]
      cmds.sets("%s.f[%s:%s]" % (model, start, end), e=1, forceElement=sg)