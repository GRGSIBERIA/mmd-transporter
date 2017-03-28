#-*- encoding: utf-8

import maya.OpenMaya
import maya.cmds

import util

class EstablishGenerator:
  
  def __init__(self, mmdData):
    self.mmdData = mmdData


  def _makeExpressionCode(self, target, emitter, axisName, power):
    s = ""
    for axis in ["X", "Y", "Z"]:
      s += "%s.%s%s = %s.%s%s * %s;" % (target, axisName, axis, emitter, axisName, axis, power)
      s += "\n"
    return s


  def _makeExpression(self, bones, jointNames, i, axisName):
    eIndex = bones[i].effect_index
    factor = bones[i].effect_factor
    expression = self._makeExpressionCode(jointNames[i], jointNames[eIndex], axisName, factor)
    maya.cmds.expression(s=expression, name="%s_%s_E" % (jointNames[i], axisName))


  def generate(self, jointNames):
    bones = self.mmdData.bones
    for i in range(len(bones)):
      establishFlag = False
      if bones[i].getExternalRotationFlag():
        self._makeExpression(bones, jointNames, i, "rotate")
        establishFlag = True

      if bones[i].getExternalTranslationFlag():
        self._makeExpression(bones, jointNames, i, "translate")
        establishFlag = True

      util.setFloat(jointNames[i], "establishFactor", bones[i].effect_factor)
      eIndex = bones[i].effect_index
      util.setString(jointNames[i], "establishParent", jointNames[eIndex])
      util.setBoolean(jointNames[i], "enableEstablish", establishFlag)