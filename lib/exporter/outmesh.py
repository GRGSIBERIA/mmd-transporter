#-*- encoding: utf-8

import maya.cmds
import maya.OpenMaya

import pymeshio
import pymeshio.pmx

import mesh

class OutMesh:

  def __init__(self, mmdModel, transform):
    self.mmdModel = mmdModel
    self.transform = transform
    self.mesh = mesh.Mesh(transform)


  def generate(self):
    pass