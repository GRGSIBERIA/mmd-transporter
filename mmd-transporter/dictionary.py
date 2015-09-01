#-*- encoding: utf-8

from hepburn import *

class Dictionary:
    def __getNames(datas):
        dict = []
        for data in datas:
            dict.append(hepburn(data.name))
        return dict

    def __init__(self, mmdData):
        self.materials  = __getNames(mmdData.materials)
        self.bones      = __getNames(mmdData.bones)
        self.joints     = __getNames(mmdData.joints)
        self.rigidbodies= __getNames(mmdData.rigidbodies)
        self.morphs     = __getNames(mmdData.morphs)