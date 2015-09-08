#-*- encoding: utf-8

from hepburn import *

class Dictionary:
    def __toString(self, datas):
        str_arr = [x.name for x in datas]
        return reduce(lambda x,y:x+u","+y, str_arr)

    def __getNames(self, datas):
        string = self.__toString(datas)
        hepped = hepburn(string)

        dict = []
        for data in hepped.split(","):
            dict.append(data)
        return dict

    def __init__(self, mmdData):
        self.materials  = self.__getNames(mmdData.materials)
        self.bones      = self.__getNames(mmdData.bones)
        self.joints     = self.__getNames(mmdData.joints)
        self.rigidbodies= self.__getNames(mmdData.rigidbodies)
        self.morphs     = self.__getNames(mmdData.morphs)