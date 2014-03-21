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

  @classmethod
  def syntaxCreator(cls):
    syntax = maya.OpenMaya.MSyntax()
    syntax.addFlag("-m", "-mesh", maya.OpenMaya.MSyntax.kNoArg)
    syntax.addFlag("-ma","-material", maya.OpenMaya.MSyntax.kNoArg)
    syntax.addFlag("-fm","-faceMaterial", maya.OpenMaya.MSyntax.kNoArg)
    syntax.addFlag("-b", "-bone", maya.OpenMaya.MSyntax.kNoArg)
    syntax.addFlag("-s", "-skinning", maya.OpenMaya.MSyntax.kNoArg)
    syntax.addFlag("-w", "-weight", maya.OpenMaya.MSyntax.kNoArg)
    return syntax

  def doIt(self, args):
    try:
      argData = maya.OpenMaya.MArgDatabase(self.syntax(), args)
    except: 
      pass
    else:
      csv_file_path = cmds.fileDialog2(dialogStyle=2, fileFilter="*.csv", okCaption="Select")[0]

      MMDTransporter.csvFilePath = csv_file_path
      poly = cmds.createNode('transform')
      mesh = cmds.createNode('mesh', parent=poly)
      cmds.sets(mesh, add='initialShadingGroup')
      plugin = cmds.createNode('transportedMMD1')
      cmds.connectAttr(plugin + '.outputMesh', mesh + '.inMesh')
      #polyNormal -normalMode 0 -userNormalMode 0 -ch 1 transform1;
      cmds.polyNormal(poly, normalMode=0, userNormalMode=0, ch=1)  # 表示が変になるのでノーマルを逆転

      if argData.isFlagSet("-m"):
        return True

      # マテリアル作成
      records = CSVImporter().toRowList(csv_file_path)
      mg = MaterialGenerator(records, csv_file_path)
      shader_groups = mg.generate()

      if argData.isFlagSet("-ma"):
        return True

      # マテリアル適用
      fmg = FaceMaterialGenerator()
      fmg.generate(records, mesh, shader_groups)

      if argData.isFlagSet("-fm"):
        return True

      # ボーン配置
      bg = BoneGenerator()
      bone_objs, bones, root_name = bg.generate(records)
      
      #cmds.select(bone_objs[root_name])
      #cmds.joint(e=True, oj="xyz", secondaryAxisOrient="yup", ch=True, zso=True)
      #joint -e  -oj xyz -secondaryAxisOrient yup -ch -zso;

      if argData.isFlagSet("-b"):
        return True

      # スキニング
      cmds.select(poly)
      cmds.select(bone_objs[root_name], tgl=True)
      cmds.SmoothBindSkin()

      if argData.isFlagSet("-s"):
        return True

      # ウェイト
      histories = cmds.listHistory(poly)
      skin_cluster = cmds.ls(histories, type="skinCluster")[0]
      SkinningGenerator().generate(records, bone_objs, bones, poly, skin_cluster)

      if argData.isFlagSet("-w"):
        return True

      return True