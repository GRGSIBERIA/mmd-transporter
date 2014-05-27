#-*- encoding: utf-8
import pymeshio.pmx.reader
import pymeshio.pmd.reader
import kakasi
import sys
import os.path
import csv


def translate(dictionary, names):
  kana = kakasi.wakachi(names)
  romaji = kakasi.hepburn(kana).replace(u" ", u"_").replace(u"^", "_")

  nameArray = names.split(u",")
  romajiArray = romaji.replace(u"_,", u",").replace(u",_", u",").split(u",")

  for i in range(len(nameArray)):
    dictionary.writerow([nameArray[i].encode('sjis'), romajiArray[i].encode('sjis')])


def makeCSV(path, directory, array):
  csvfile = open(directory + path, "wb")
  dictionary = csv.writer(csvfile)
  nameArray = []
  for e in array:
    nameArray.append(e.name)
  allNames = ",".join(nameArray)
  translate(dictionary, allNames)
  csvfile.close()


def makeCSVs(directory, mmdData):
  makeCSV("\\bonedict.csv", directory, mmdData.bones)
  makeCSV("\\skindict.csv", directory, mmdData.morphs)
  makeCSV("\\materialdict.csv", directory, mmdData.materials)
  makeCSV("\\rigiddict.csv", directory, mmdData.rigidbodies)
  makeCSV("\\morphdict.csv", directory, mmdData.morphs)


def trace(argv):
  for arg in argv:
    path, ext = os.path.splitext(arg)
    ext = ext.lower()
    mmdData = None
    if ext == ".pmd":
      mmdData = pymeshio.pmd.reader.read_from_file(arg)
    if ext == ".pmx":
      mmdData = pymeshio.pmx.reader.read_from_file(arg)
    else:
      raise "do not PMD/PMX"

    directory = os.path.dirname(arg)
    makeCSVs(directory, mmdData)

if __name__ == "__main__":
  trace(sys.argv[1:])