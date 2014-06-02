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
    result, errData = process.communicate()
    return result


  def __divideString(self, string):
    lines = string.split("\n")
    for line in lines:
      elems = line.split(",")
      if len(elems) <= 1:
        continue
      t = elems[0]
      en = elems[1]

      if t == "Material":
        self.materials.append(en)
      elif t == "Bone":
        self.bones.append(en)
      elif t == "Joint":
        self.joints.append(en)
      elif t == "Rigid":
        self.rigidbodies.append(en)
      elif t == "Morph":
        self.morphs.append(en)


  def __init__(self, mmdData):
    path = mmdData.path
    stdout = self.__startProcess(path)
    self.materials = []
    self.bones = []
    self.joints = []
    self.rigidbodies = []
    self.morphs = []
    self.__divideString(stdout)