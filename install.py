#-*- encoding: utf-8
import os
import sys
import shutil

try:
  abspath = os.path.abspath(__file__)
  directory = os.path.dirname(abspath)
  batchPath = directory + "\\makedict.bat"
  programPath = directory + "\\lib\\makedict.py"
  f = open(batchPath, "w")
  f.write("python \"" + programPath + "\" \"%1\"\n")
  f.write("pause\n")
  f.close()
  print "Completed create makedict.bat."
except Exception as e:
  print "Instaling Failed!!!"
  print "What's happen?"
  print ""

try:
  username = os.environ.get("USERNAME")
  hikPath = "C:\\Users\\%s\\AppData\\Roaming\\Autodesk\\HIKCharacterizationTool4\\template" % username
  shutil.copy("MMD HumanIK.xml", hikPath)
  print "Completed to copy MMD HumanIK.xml."
except Exception as e:
  print "Instaling Failed!!!"
  print "Failed to copy MMD HumanIK.xml."
  print "Please copy and paste MMD HumanIK.xml."
  print ""

try:
  shutil.copytree("kakasi", "C:/kakasi")
  print "Completed to copy kakasi directory."
except Exception as e:
  print "Instaling Failed!!!"
  print "C:/kakasi directory was existing."
  print "Please remove C:/kakasi directory or copy and paste kakasi directory."
  print ""

print ""
print "Installing successful."
print "Please press any key."
raw_input()