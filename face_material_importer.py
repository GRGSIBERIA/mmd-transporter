#-*- encoding: utf-8
import maya.cmds as cmds

class FaceMaterialGenerator:
  def __init__(self):
    pass

  def generate(self, records, model, shader_groups):
    cnt = 0
    for row in records:
      if row[0] == "Face":
        mat_name = row[1]
        sg = shader_groups[mat_name]
        cmds.sets("%s.f[%s]" % (model, cnt), e=1, forceElement=sg)
        cnt += 1