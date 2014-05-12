#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

class Tagger(object):
    def __init__(self, opts = []):
        self.set_opts(opts)

    def set_opts(self, opts = []):
        _args = [ctypes.c_char_p("kakasi")]

        for opt in opts:
            if opt == 'kakasi':
                continue
            else:
                if opt.startswith('-'):
                    _args.append(ctypes.c_char_p(opt))
                else:
                    _args.append(ctypes.c_char_p('-' + opt))

        argArray = ctypes.c_char_p * len(_args)
        args = argArray(*_args)        

        self.kakasi = ctypes.cdll.LoadLibrary("kakasi.dll")
        self.kakasi.kakasi_getopt_argv(len(_args), args)

    def parse(self, ustr):
        kakasi_do = self.kakasi.kakasi_do
        kakasi_do.restype = ctypes.c_char_p

        eres = kakasi_do(ctypes.c_char_p(ustr.encode('euc-jp', 'ignore')))

        return unicode(eres, 'euc-jp', 'ignore').strip()

def hepburn(ustr):
    k = Tagger(['-Ha', '-Ka', '-Ja', '-Ea', '-ka'])
    return k.parse(ustr)

def hiragana(ustr):
    k = Tagger(['-AH', '-KH', '-JH', '-EH', '-kH'])
    return k.parse(ustr)

def katakana(ustr):
    k = Tagger(['-HK', '-AK', '-JK', '-EK'])
    return k.parse(ustr)

def kunrei(ustr):
    k = Tagger(['-rk', '-Ha', '-Ka', '-Ja', '-Ea', '-ka'])
    return k.parse(ustr)

def wakachi(ustr):
    k = Tagger(['-w'])
    return k.parse(ustr)

