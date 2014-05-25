#-*- encoding: utf-8

class MmdBoneListWindow:

  def __init__(self):
    pass


  def _layout(self):
    maya.cmds.columnLayout()

    


  def show(self):
    title = "MMD BoneList Window"
    window = maya.cmds.window(\
      t=title, wh=(400, 800),\
      menuBar=True)

    self._layout()

    maya.cmds.dockControl(\
      l=title, fl=True, content=window,\
      w=400, area="left", allowedArea=("left", "right"))