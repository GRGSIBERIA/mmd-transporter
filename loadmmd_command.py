#-*- encoding: utf-8
class LoadMMDCommand(maya.OpenMayaMPx.MPxCommand):
  def __init__(self):
    maya.OpenMayaMPx.MPxCommand.__init__(self)

  def doIt(self, args):
    print "hello"

  @classmethod
  def cmdCreator(cls):
    return maya.OpenMayaMPx.asMPxPtr(cls())