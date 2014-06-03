#-*- encoding: utf-8
import sys
import os.path
import maya.OpenMayaMPx
import maya.cmds

import pymeshio.pmx.reader
import pymeshio.pmd.reader


class SaveMMD(maya.OpenMayaMPx.MPxCommand):

  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  @classmethod
  def syntaxCreator(cls):
    syntax = maya.OpenMaya.MSyntax()
    return syntax

  