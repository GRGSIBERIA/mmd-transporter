#-*- encoding: utf-8
import maya.cmds
import maya.OpenMaya
import copy

class JointOrientAdjuster:

  def __init__(self):
    pass


  def _layout(self):
    pass
    

  def show(self):
    self.window = maya.cmds.window(t="Joint Orient Adjuster", w=300, h=300)

    self._layout()

    maya.cmds.showWindow(self.window)


def show():
  joa = JointOrientAdjuster()
  joa.show()

show()