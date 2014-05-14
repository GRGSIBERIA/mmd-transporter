#-*- encoding: utf-8
import csv

def openCSV(directory, filename):
  nameDict = []
  dictFlag = True
  try:
    f = open(directory + "\\" + filename, "rb")
    csvfile = csv.reader(f)
    for row in csvfile:
      nameDict.append(row[1])
    f.close()
  except:
    dictFlag = False
    print "bonedict.csv not found."
  return nameDict, dictFlag