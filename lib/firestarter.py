#-*- encoding: utf-8
import sys
import pymeshio.pmx.reader
import pymeshio.pmd.reader
import os.path
import kakasi

def readmmd(path):
  mmd = None
  ext = os.path.splitext(path)[1].lower()
  if ext == u".pmx":
    mmd = pymeshio.pmx.reader.read_from_file(path)
  elif ext == u".pmd":
    mmd = pymeshio.pmd.reader.read_from_file(path)
  return mmd


def collectname(arr):
  c = ""
  for e in arr:
    c += u"%s," % e.name
  return c


def tohepburn(namestr):
  namestr = kakasi.wakachi(namestr)
  names = kakasi.hepburn(namestr)
  names = names.replace(u"^", u"_").replace(u" ", u"_")
  names = names.replace(u"_,", u",").replace(u",_", u",")
  names = names.replace(u"___", u"_")
  return names


def combine(t, arr, spl):
  result = u""
  for i in range(len(arr)):
    result += u"%s,%s,\n" % (t, spl[i])
  return result


def collect(t, arr):
  c = collectname(arr)
  c = tohepburn(c)
  spl = c.split(u",")
  return combine(t, arr, spl)
  

def main(path):
  mmd = readmmd(path)
  print collect(u"Material", mmd.materials)
  print collect(u"Morph", mmd.morphs)
  print collect(u"Bone", mmd.bones)
  print collect(u"Rigid", mmd.rigidbodies)
  print collect(u"Joint", mmd.joints)


if __name__ == "__main__":
  main(sys.argv[1])