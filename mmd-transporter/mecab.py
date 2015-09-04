#-*- encoding: utf-8

import os
import subprocess
import locale
from subprocess import PIPE, Popen

class MeCabBinding:
    def __init__(self):
        self.mecab_path = os.environ.get("MECAB_PATH") + "\\bin\\mecab.exe"
        print self.mecab_path

    def doHepburn(self, strings):
        command = u"echo %s | \"%s\" -Oyomi" % (strings, self.mecab_path)
        process = Popen(command.encode(locale.getpreferredencoding()), stdin=PIPE, stdout=PIPE, shell=True)
        (result, errcode) = process.communicate()
        return result