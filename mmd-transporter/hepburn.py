# -*- coding: utf-8 -*-
import MeCab
import re

"""���ȁ̃��[�}����ϊ�����"""

def _make_kana_convertor():
    """�Ђ炪�ȁ̃J�^�J�i�ϊ�������"""
    kata = {
        '�A':'��', '�C':'��', '�E':'��', '�G':'��', '�I':'��',
        '�J':'��', '�L':'��', '�N':'��', '�P':'��', '�R':'��',
        '�T':'��', '�V':'��', '�X':'��', '�Z':'��', '�\':'��',
        '�^':'��', '�`':'��', '�c':'��', '�e':'��', '�g':'��',
        '�i':'��', '�j':'��', '�k':'��', '�l':'��', '�m':'��',
        '�n':'��', '�q':'��', '�t':'��', '�w':'��', '�z':'��',
        '�}':'��', '�~':'��', '��':'��', '��':'��', '��':'��',
        '��':'��', '��':'��', '��':'��', '��':'��', '��':'��',
        '��':'��', '��':'��', '��':'��', '��':'��', '��':'��',
        '��':'��',
        
        '�K':'��', '�M':'��', '�O':'��', '�Q':'��', '�S':'��',
        '�U':'��', '�W':'��', '�Y':'��', '�[':'��', '�]':'��',
        '�_':'��', '�a':'��', '�d':'��', '�f':'��', '�h':'��',
        '�o':'��', '�r':'��', '�u':'��', '�x':'��', '�{':'��',
        '�p':'��', '�s':'��', '�v':'��', '�y':'��', '�|':'��',
        
        '�@':'��', '�B':'��', '�D':'��', '�F':'��', '�H':'��',
        '��':'��', '��':'��', '��':'��',
        '��':'&#12436;', '�b':'��', '��':'��', '��':'��',
        }
    
    # �Ђ炪�� �� �J�^�J�i �̃f�B�N�V���i��������
    hira = dict([(v, k) for k, v in kata.items() ])
    
    re_hira2kata = re.compile("|".join(map(re.escape, hira)))
    re_kata2hira = re.compile("|".join(map(re.escape, kata)))
    
    def _hiragana2katakana(text):
        return re_hira2kata.sub(lambda x: hira[x.group(0)], text)
    
    def _katakana2hiragana(text):
        return re_kata2hira.sub(lambda x: kata[x.group(0)], text)
    
    return (_hiragana2katakana, _katakana2hiragana)


hiragana2katakana, katakana2hiragana = _make_kana_convertor()

################################################################################

def _make_romaji_convertor():
    """���[�}���̂��ȕϊ�������"""
    master = {
        'a'  :'�A', 'i'  :'�C', 'u'  :'�E', 'e'  :'�G', 'o'  :'�I',
        'ka' :'�J', 'ki' :'�L', 'ku' :'�N', 'ke' :'�P', 'ko' :'�R',
        'sa' :'�T', 'shi':'�V', 'su' :'�X', 'se' :'�Z', 'so' :'�\',
        'ta' :'�^', 'chi':'�`', 'tu' :'�c', 'te' :'�e', 'to' :'�g',
        'na' :'�i', 'ni' :'�j', 'nu' :'�k', 'ne' :'�l', 'no' :'�m',
        'ha' :'�n', 'hi' :'�q', 'fu' :'�t', 'he' :'�w', 'ho' :'�z',
        'ma' :'�}', 'mi' :'�~', 'mu' :'��', 'me' :'��', 'mo' :'��',
        'ya' :'��', 'yu' :'��', 'yo' :'��',
        'ra' :'��', 'ri' :'��', 'ru' :'��', 're' :'��', 'ro' :'��',
        'wa' :'��', 'wo' :'��', 'n'  :'��', 'vu' :'��',
        'ga' :'�K', 'gi' :'�M', 'gu' :'�O', 'ge' :'�Q', 'go' :'�S',
        'za' :'�U', 'ji' :'�W', 'zu' :'�Y', 'ze' :'�[', 'zo' :'�]',
        'da' :'�_', 'di' :'�a', 'du' :'�d', 'de' :'�f', 'do' :'�h',
        'ba' :'�o', 'bi' :'�r', 'bu' :'�u', 'be' :'�x', 'bo' :'�{',
        'pa' :'�p', 'pi' :'�s', 'pu' :'�v', 'pe' :'�y', 'po' :'�|',
        
        'kya':'�L��', 'kyi':'�L�B', 'kyu':'�L��', 'kye':'�L�F', 'kyo':'�L��',
        'gya':'�M��', 'gyi':'�M�B', 'gyu':'�M��', 'gye':'�M�F', 'gyo':'�M��',
        'sha':'�V��',               'shu':'�V��', 'she':'�V�F', 'sho':'�V��',
        'ja' :'�W��',               'ju' :'�W��', 'je' :'�W�F', 'jo' :'�W��',
        'cha':'�`��',               'chu':'�`��', 'che':'�`�F', 'cho':'�`��',
        'dya':'�a��', 'dyi':'�a�B', 'dyu':'�a��', 'dhe':'�f�F', 'dyo':'�a��',
        'nya':'�j��', 'nyi':'�j�B', 'nyu':'�j��', 'nye':'�j�F', 'nyo':'�j��',
        'hya':'�q��', 'hyi':'�q�B', 'hyu':'�q��', 'hye':'�q�F', 'hyo':'�q��',
        'bya':'�r��', 'byi':'�r�B', 'byu':'�r��', 'bye':'�r�F', 'byo':'�r��',
        'pya':'�s��', 'pyi':'�s�B', 'pyu':'�s��', 'pye':'�s�F', 'pyo':'�s��',
        'mya':'�~��', 'myi':'�~�B', 'myu':'�~��', 'mye':'�~�F', 'myo':'�~��',
        'rya':'����', 'ryi':'���B', 'ryu':'����', 'rye':'���F', 'ryo':'����',
        'fa' :'�t�@', 'fi' :'�t�B',               'fe' :'�t�F', 'fo' :'�t�H',
        'wi' :'�E�B', 'we' :'�E�F', 
        'va' :'���@', 'vi' :'���B', 've' :'���F', 'vo' :'���H',
        
        'kwa':'�N�@', 'kwi':'�N�B', 'kwu':'�N�D', 'kwe':'�N�F', 'kwo':'�N�H',
        'kha':'�N�@', 'khi':'�N�B', 'khu':'�N�D', 'khe':'�N�F', 'kho':'�N�H',
        'gwa':'�O�@', 'gwi':'�O�B', 'gwu':'�O�D', 'gwe':'�O�F', 'gwo':'�O�H',
        'gha':'�O�@', 'ghi':'�O�B', 'ghu':'�O�D', 'ghe':'�O�F', 'gho':'�O�H',
        'swa':'�X�@', 'swi':'�X�B', 'swu':'�X�D', 'swe':'�X�F', 'swo':'�X�H',
        'swa':'�X�@', 'swi':'�X�B', 'swu':'�X�D', 'swe':'�X�F', 'swo':'�X�H',
        'zwa':'�Y��', 'zwi':'�Y�B', 'zwu':'�Y�D', 'zwe':'�Y�F', 'zwo':'�Y�H',
        'twa':'�g�@', 'twi':'�g�B', 'twu':'�g�D', 'twe':'�g�F', 'two':'�g�H',
        'dwa':'�h�@', 'dwi':'�h�B', 'dwu':'�h�D', 'dwe':'�h�F', 'dwo':'�h�H',
        'mwa':'����', 'mwi':'���B', 'mwu':'���D', 'mwe':'���F', 'mwo':'���H',
        'bwa':'�r��', 'bwi':'�r�B', 'bwu':'�r�D', 'bwe':'�r�F', 'bwo':'�r�H',
        'pwa':'�v��', 'pwi':'�v�B', 'pwu':'�v�D', 'pwe':'�v�F', 'pwo':'�v�H',
        'phi':'�v�B', 'phu':'�v�D', 'phe':'�v�F', 'pho':'�t�H',
        }
    
    
    romaji_asist = {
        'si' :'�V'  , 'ti' :'�`'  , 'hu' :'�t' , 'zi':'�W',
        'sya':'�V��', 'syu':'�V��', 'syo':'�V��',
        'tya':'�`��', 'tyu':'�`��', 'tyo':'�`��',
        'cya':'�`��', 'cyu':'�`��', 'cyo':'�`��',
        'jya':'�W��', 'jyu':'�W��', 'jyo':'�W��', 'pha':'�t�@', 
        'qa' :'�N�@', 'qi' :'�N�B', 'qu' :'�N�D', 'qe' :'�N�F', 'qo':'�N�H',
        
        'ca' :'�J', 'ci':'�V', 'cu':'�N', 'ce':'�Z', 'co':'�R',
        'la' :'��', 'li':'��', 'lu':'��', 'le':'��', 'lo':'��',

        'mb' :'��', 'py':'�p�C', 'tho': '�\', 'thy':'�e�B', 'oh':'�I�E',
        'by':'�r�B', 'cy':'�V�B', 'dy':'�f�B', 'fy':'�t�B', 'gy':'�W�B',
        'hy':'�V�[', 'ly':'���B', 'ny':'�j�B', 'my':'�~�B', 'ry':'���B',
        'ty':'�e�B', 'vy':'���B', 'zy':'�W�B',
        
        'b':'�u', 'c':'�N', 'd':'�h', 'f':'�t'  , 'g':'�O', 'h':'�t', 'j':'�W',
        'k':'�N', 'l':'��', 'm':'��', 'p':'�v'  , 'q':'�N', 'r':'��', 's':'�X',
        't':'�g', 'v':'��', 'w':'�D', 'x':'�N�X', 'y':'�B', 'z':'�Y',
        }
    

    kana_asist = { 'a':'�@', 'i':'�B', 'u':'�D', 'e':'�F', 'o':'�H', }
    
    
    def __romaji2kana():
        romaji_dict = {}
        for tbl in master, romaji_asist:
            for k, v in tbl.items(): romaji_dict[k] = v
        
        romaji_keys = romaji_dict.keys()
        romaji_keys.sort(key=lambda x:len(x), reverse=True)
        
        re_roma2kana = re.compile("|".join(map(re.escape, romaji_keys)))
        # m �̌��Ƀo�s�A�p�s�̂Ƃ��� "��" �ƕϊ�
        rx_mba = re.compile("m(b|p)([aiueo])")
        # �q������������ "�b" �ƕϊ�
        rx_xtu = re.compile(r"([bcdfghjklmpqrstvwxyz])\1")
        # �ꉹ���������� "�[" �ƕϊ�
        rx_a__ = re.compile(r"([aiueo])\1")
        
        def _romaji2katakana(text):
            result = text.lower()
            result = rx_mba.sub(r"��\1\2", result)
            result = rx_xtu.sub(r"�b\1"  , result)
            result = rx_a__.sub(r"\1�["  , result)
            return re_roma2kana.sub(lambda x: romaji_dict[x.group(0)], result)
        
        def _romaji2hiragana(text):
            result = _romaji2katakana(text)
            return katakana2hiragana(result)
        
        return _romaji2katakana, _romaji2hiragana
    
    
    def __kana2romaji():
        kana_dict = {}
        for tbl in master, kana_asist:
            for k, v in tbl.items(): kana_dict[v] = k

        kana_keys = kana_dict.keys()
        kana_keys.sort(key=lambda x:len(x), reverse=True)
        
        re_kana2roma = re.compile("|".join(map(re.escape, kana_keys)))
        rx_xtu = re.compile("�b(.)") # ������ "�b" �͒���̕������Q��ɕϊ�
        rx_ltu = re.compile("�b$"  ) # �Ō�̏����� "�b" �͏���(?)
        rx_er  = re.compile("(.)�[") # "�["�͒��O�̕������Q��ɕϊ�
        rx_n   = re.compile(r"n(b|p)([aiueo])") # n �̌�낪 �o�s�A�p�s �Ȃ� m �ɏC��
        rx_oo  = re.compile(r"([aiueo])\1")      # oosaka �� osaka
        
        def _kana2romaji(text):
            result = hiragana2katakana(text)
            result = re_kana2roma.sub(lambda x: kana_dict[x.group(0)], result)
            result = rx_xtu.sub(r"\1\1" , result)
            result = rx_ltu.sub(r""     , result)
            result = rx_er.sub (r"\1\1" , result)
            result = rx_n.sub  (r"m\1\2", result)
            result = rx_oo.sub (r"\1"   , result)
            return result
        return _kana2romaji
    
    a, b = __romaji2kana()
    c    = __kana2romaji()
    
    return  a, b, c


romaji2katakana, romaji2hiragana, kana2romaji = _make_romaji_convertor()

################################################################################

def hepburn(name):
	yomi = MeCab.Tagger("-Oyomi")
	return kana2romaji(name)

