#-*- encoding: utf-8
import os.path
import csv
import subprocess
import locale
from subprocess import Popen, PIPE

class DictMaker:

  def __startProcess(self, path):
    programDirectory = os.path.abspath(os.path.dirname(__file__))
    programDirectory += u"\\firestarter.py"

    result = ""
    command = u"Python %s \"%s\"" % (programDirectory, path)
    process = subprocess.Popen(command.encode(locale.getpreferredencoding()), stdout=PIPE)
    while 1:
      line = process.stdout.readline()
      if not line:
        break
    return result


  def __divideString(self, string):
    lines = string.split(u"\n")
    for line in lines:
      elems = line.split(u",")
      if len(elems) <= 1:
        continue
      t = elems[0]
      en = elems[1]

      if t == u"Material":
        self.materials.append(en)
      elif t == u"Bone":
        self.bones.append(en)
      elif t == u"Joint":
        self.joints.append(en)
      elif t == u"Rigidbody":
        self.rigidbodies.append(en)
      elif t == u"Morph":
        self.morphs.append(en)


  def __init__(self, mmdData):
    path = mmdData.path
    stdout = self.__startProcess(path)
    self.materials = []
    self.bones = []
    self.joints = []
    self.rigidbodies = []
    self.morphs = []
    #print stdout
    self.__divideString(stdout)