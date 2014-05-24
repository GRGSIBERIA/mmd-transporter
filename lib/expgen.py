#-*- encoding: utf-8

import os.path
import maya.cmds
import maya.OpenMaya

import filemanager
import util

class ExpressionGenerator:

  def __init__(self, mmdData, filePath):
    self.mmdData = mmdData
    self.directory = os.path.dirname(filePath)
    self.nameDict, self.dictFlag = filemanager.openCSV(self.directory, "morphdict.csv")


  def _duplicateMesh(self):
    morphs = self.mmdData.morphs
    morphNames = []
    morphPanelCounts = [0, 0, 0, 0, 0]
    for i in range(len(morphs)):
      morph = morphs[i]
      name = "expression"
      if self.dictFlag:
        name = "exp_" + self.nameDict[i]
      morphName = maya.cmds.duplicate(self.polyName, n=name)[0]
      util.setJpName(morphName, morphs[i].name)
      morphNames.append(morphName)

      morphPanelCounts[morph.panel] += 1
      count = morphPanelCounts[morph.panel]
      maya.cmds.select(morphName)
      maya.cmds.move(8 * count, morph.panel * 8, -(morph.panel * 8))
    return morphNames


  def _createDisplayLayer(self, morphNames):
    morphs = self.mmdData.morphs
    panels = ["eyebrow_group", "eye_group", "mouth_group", "other_group"]
    panelJpNames = [u"眉", u"目", u"口", u"その他"]
    groups = []
    for panel in range(4):
      maya.cmds.select(d=True)
      for i in range(len(morphs)):
        if morphs[i].panel == panel + 1:
          maya.cmds.select(morphNames[i], tgl=True)
      groupName = maya.cmds.group(name=panels[panel])
      util.setString(groupName, "expression", panelJpNames[panel])
      maya.cmds.setAttr("%s.v" % groupName, 0)
      groups.append(groupName)
    return groups


  def _structVertexMorph(self, morph, morphName):
    for offset in morph.offsets:
      path = "%s.vtx[%s]" % (morphName, offset.vertex_index)
      pos = offset.position_offset
      maya.cmds.move(pos.x, pos.y, -pos.z, path, r=True)


  def _structUVMorph(self, morph, morphName):
    for offset in morph.offsets:
      #path = "%s.uv[%s]" % (morphNames, offset.)  # UVモーフが実装されてなかった
      pass

  def _doOffsetsDuplicateModel(self, morphNames):
    morphs = self.mmdData.morphs
    for i in range(len(morphs)):
      if morphs[i].morph_type == 0:   # グループ
        pass
      elif morphs[i].morph_type == 1: # 頂点
        self._structVertexMorph(morphs[i], morphNames[i])
      elif morphs[i].morph_type == 2: # ボーン
        pass
      elif morphs[i].morph_type == 3: # UV  UVモーフはなぜかpymeshioで実装されてない
        pass
      elif morphs[i].morph_type == 4: # UV1
        pass
      elif morphs[i].morph_type == 5: # UV2
        pass
      elif morphs[i].morph_type == 6: # UV3
        pass
      elif morphs[i].morph_type == 7: # UV4
        pass
      elif morphs[i].morph_type == 8: # 材質
        pass


  def _appendBlendShapes(self, polyName, morphNames):
    maya.cmds.select(d=True)
    for morphName in morphNames:
      maya.cmds.select(morphName, tgl=True)
    maya.cmds.select(polyName, tgl=True)

    blendShapeNode = maya.cmds.blendShape()[0]
    morphs = self.mmdData.morphs

    # ここでパネル用のアトリビュートをこっそり追加する
    morphLength = len(morphs)
    maya.cmds.select(blendShapeNode)
    maya.cmds.addAttr(longName="panel", numberOfChildren=morphLength, attributeType="compound")
    for i in range(morphLength):
      name = morphNames[i].replace("exp_", "panel_")
      maya.cmds.addAttr(longName=name, attributeType="long", parent="panel", defaultValue=morphs[i].panel)

  def generate(self, polyName):
    self.polyName = polyName

    morphNames = self._duplicateMesh()
    groupNames = self._createDisplayLayer(morphNames)
    self._doOffsetsDuplicateModel(morphNames)
    self._appendBlendShapes(polyName, morphNames)
    return groupNames