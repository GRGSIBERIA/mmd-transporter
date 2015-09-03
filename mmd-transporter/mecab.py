#-*- encoding: utf-8

import os
import subprocess

class MeCabBinding:
    def __init__(self):
        self.mecab_path = os.environ.get("MECAB_PATH") + "bin\\mecab.exe"
        print self.mecab_path

    def doHepburn(self, strings):
        return subprocess.check_output("echo %s | %s -Oyomi" % (strings, self.mecab_path), shell=True)