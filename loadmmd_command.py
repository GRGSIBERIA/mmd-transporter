#-*- encoding: utf-8
import maya.OpenMaya
import maya.OpenMayaMPx
import maya.cmds as cmds

from transporter import *
from material_importer import * 
from face_material_importer import *
from bone_importer import *
from skinning_importer import *

class LoadMMDCommand(maya.OpenMayaMPx.MPxCommand):
  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  @classmethod
  def cmdCreator(cls):
    return maya.OpenMayaMPx.asMPxPtr(cls())

  def doIt(self, args):
    csv_file_path = cmds.fileDialog2(dialogStyle=2, fileFilter="*.csv", okCaption="Select")[0]

    MMDTransporter.csvFilePath = csv_file_path
    poly = cmds.createNode('transform')
    mesh = cmds.createNode('mesh', parent=poly)
    cmds.sets(mesh, add='initialShadingGroup')
    spoly = cmds.createNode('transportedMMD1')
    cmds.connectAttr(spoly + '.outputMesh', mesh + '.inMesh')
    #polyNormal -normalMode 0 -userNormalMode 0 -ch 1 transform1;
    cmds.polyNormal(poly, normalMode=0, userNormalMode=0, ch=1)  # 表示が変になるのでノーマルを逆転

    records = CSVImporter().toRowList(csv_file_path)
    mg = MaterialGenerator(records, csv_file_path)
    shader_groups = mg.generate()

    # マテリアル適用
    fmg = FaceMaterialGenerator()
    fmg.generate(records, mesh, shader_groups)

    # ボーン配置
    bg = BoneGenerator()
    bone_objs, bones = bg.generate(records)

    root_name = None # ルートボーンを探索する

    cmds.select(bone_objs[root_name])
    #joint -e  -oj xyz -secondaryAxisOrient yup -ch -zso;

    # スキニング
    cmds.select(poly)
    cmds.select(bone_objs[root_name], tgl=True)
    cmds.SmoothBindSkin()

    # ウェイト
    histories = cmds.listHistory(poly)
    skin_cluster = cmds.ls(histories, type="skinCluster")[0]
    SkinningGenerator().generate(records, bone_objs, bones, poly, skin_cluster)