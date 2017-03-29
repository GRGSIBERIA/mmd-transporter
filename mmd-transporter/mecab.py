#-*- encoding: utf-8

import os
import subprocess
import locale
from subprocess import PIPE, Popen
import codecs



class MeCabBinding:
    def __init__(self):
        self.mecab_path = os.environ.get("MECAB_PATH") + "\\bin\\mecab.exe"

    def doHepburn(self, strings):
        f = open("inyomi.txt", "w")
        f.write(strings.encode("utf-8"))
        f.close()

        command = u"\"%s\" inyomi.txt -o oyomi.txt -Oyomi" % (self.mecab_path)
        process = Popen(command.encode(locale.getpreferredencoding()), stdin=PIPE, stdout=PIPE, shell=True)
        (result, errcode) = process.communicate()

        f = open("oyomi.txt", "r")
        result = f.read()
        f.close()

        return result.replace("\r\n", "")