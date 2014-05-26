#-*- encoding: utf-8
import os
import sys
import shutil

abspath = os.path.abspath(__file__)

directory = os.path.dirname(abspath)
batchPath = directory + "\\makedict.bat"
programPath = directory + "\\makedict.py"
f = open(batchPath, "w")
f.write("python \"" + programPath + "\" \"%1\"\n")
f.write("pause\n")
f.close()

shutil.copytree("kakasi", "C:/kakasi")