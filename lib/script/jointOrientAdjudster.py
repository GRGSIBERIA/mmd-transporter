#-*- encoding: utf-8
import maya.cmds
import maya.OpenMaya
import pymel.core as pm
import copy

class JointOrientControlls:

  def __init__(self):
    self.width = 340


  def _rowLayout(self, nc, funcArray):
    maya.cmds.rowLayout(nc=nc)
    for func in funcArray:
      func[0](**func[1])
    maya.cmds.setParent("..")


  def _layout(self):
    maya.cmds.columnLayout()

    maya.cmds.button(l="Set Joint", w=self.width, h=32)

    self._rowLayout(2, [
        [maya.cmds.text, {"l":"  Selected Joint  ", "w":82}],
        [maya.cmds.textField, {"editable":False}]
      ])

    self._rowLayout(2, [
        [maya.cmds.text, {"l":"  Front Direction  "}],
        [maya.cmds.textScrollList, {"w":250, "h":128}]
      ])
    
    self._rowLayout(5, [
        [maya.cmds.text, {"l":"  Front  ", "w":82}],
        [maya.cmds.button, {"l":"X", "w":32}],
        [maya.cmds.button, {"l":"Y", "w":32}],
        [maya.cmds.button, {"l":"Z", "w":32}],
        [maya.cmds.button, {"l":"+/-", "w":32}]
      ])

    self._rowLayout(5, [
        [maya.cmds.text, {"l":"  Side  ", "w":82}],
        [maya.cmds.button, {"l":"X", "w":32}],
        [maya.cmds.button, {"l":"Y", "w":32}],
        [maya.cmds.button, {"l":"Z", "w":32}],
        [maya.cmds.button, {"l":"+/-", "w":32}]
      ])
    

  def show(self):
    self.window = maya.cmds.window(t="Joint Orient Adjuster", w=self.width, h=300)

    self._layout()

    maya.cmds.showWindow(self.window)


def show():
  joa = JointOrientControlls()
  joa.show()

show()