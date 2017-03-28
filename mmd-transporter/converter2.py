# -*- coding: utf-8 -*-
# ここから拝借
# https://github.com/MiCHiLU/zenhan-py
from types import UnicodeType
from xml.sax.saxutils import escape

ASCII = 1
DIGIT = 2
KANA  = 4
ALL = ASCII | DIGIT | KANA

__version__ = '0.4'

class zenhanError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# list of ZENKAKU characters
z_ascii = [u"ａ", u"ｂ", u"ｃ", u"ｄ", u"ｅ", u"ｆ", u"ｇ", u"ｈ", u"ｉ",
           u"ｊ", u"ｋ", u"ｌ", u"ｍ", u"ｎ", u"ｏ", u"ｐ", u"ｑ", u"ｒ",
           u"ｓ", u"ｔ", u"ｕ", u"ｖ", u"ｗ", u"ｘ", u"ｙ", u"ｚ",
           u"Ａ", u"Ｂ", u"Ｃ", u"Ｄ", u"Ｅ", u"Ｆ", u"Ｇ", u"Ｈ", u"Ｉ",
           u"Ｊ", u"Ｋ", u"Ｌ", u"Ｍ", u"Ｎ", u"Ｏ", u"Ｐ", u"Ｑ", u"Ｒ",
           u"Ｓ", u"Ｔ", u"Ｕ", u"Ｖ", u"Ｗ", u"Ｘ", u"Ｙ", u"Ｚ",
           u"！", u"”", u"＃", u"＄", u"％", u"＆", u"’", u"（", u"）",
           u"＊", u"＋", u"，", u"－", u"．", u"／", u"：", u"；", u"＜",
           u"＝", u"＞", u"？", u"＠", u"［", u"￥", u"］", u"＾", u"＿",
           u"‘", u"｛", u"｜", u"｝", u"～", u"　"]

z_digit = [u"０", u"１", u"２", u"３", u"４",
           u"５", u"６", u"７", u"８", u"９"]

z_kana = [u"ア", u"イ", u"ウ", u"エ", u"オ",
          u"カ", u"キ", u"ク", u"ケ", u"コ",
          u"サ", u"シ", u"ス", u"セ", u"ソ",
          u"タ", u"チ", u"ツ", u"テ", u"ト",
          u"ナ", u"ニ", u"ヌ", u"ネ", u"ノ",
          u"ハ", u"ヒ", u"フ", u"ヘ", u"ホ",
          u"マ", u"ミ", u"ム", u"メ", u"モ",
          u"ヤ", u"ユ", u"ヨ",
          u"ラ", u"リ", u"ル", u"レ", u"ロ",
          u"ワ", u"ヲ", u"ン",
          u"ァ", u"ィ", u"ゥ", u"ェ", u"ォ",
          u"ッ", u"ャ", u"ュ", u"ョ", u"ヴ",
          u"ガ", u"ギ", u"グ", u"ゲ", u"ゴ",
          u"ザ", u"ジ", u"ズ", u"ゼ", u"ゾ",
          u"ダ", u"ヂ", u"ヅ", u"デ", u"ド",
          u"バ", u"ビ", u"ブ", u"ベ", u"ボ",
          u"パ", u"ピ", u"プ", u"ペ", u"ポ",
          u"。", u"、", u"・", u"゛", u"゜", u"「", u"」", u"ー"]

# list of HANKAKU characters
h_ascii = [u"a", u"b", u"c", u"d", u"e", u"f", u"g", u"h", u"i",
           u"j", u"k", u"l", u"m", u"n", u"o", u"p", u"q", u"r",
           u"s", u"t", u"u", u"v", u"w", u"x", u"y", u"z",
           u"A", u"B", u"C", u"D", u"E", u"F", u"G", u"H", u"I",
           u"J", u"K", u"L", u"M", u"N", u"O", u"P", u"Q", u"R",
           u"S", u"T", u"U", u"V", u"W", u"X", u"Y", u"Z",
           u"!", u'"', u"#", u"$", u"%", u"&", u"'", u"(", u")",
           u"*", u"+", u",", u"-", u".", u"/", u":", u";", u"<",
           u"=", u">", u"?", u"@", u"[", u"\\", u"]", u"^", u"_",
           u"`", u"{", u"|", u"}", u"~", u" "]

he_ascii = [escape(i) for i in h_ascii]

h_digit = [u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9"]

h_kana = [u"ｱ", u"ｲ", u"ｳ", u"ｴ", u"ｵ",
          u"ｶ", u"ｷ", u"ｸ", u"ｹ", u"ｺ",
          u"ｻ", u"ｼ", u"ｽ", u"ｾ", u"ｿ",
          u"ﾀ", u"ﾁ", u"ﾂ", u"ﾃ", u"ﾄ",
          u"ﾅ", u"ﾆ", u"ﾇ", u"ﾈ", u"ﾉ",
          u"ﾊ", u"ﾋ", u"ﾌ", u"ﾍ", u"ﾎ",
          u"ﾏ", u"ﾐ", u"ﾑ", u"ﾒ", u"ﾓ",
          u"ﾔ", u"ﾕ", u"ﾖ",
          u"ﾗ", u"ﾘ", u"ﾙ", u"ﾚ", u"ﾛ",
          u"ﾜ", u"ｦ", u"ﾝ",
          u"ｧ", u"ｨ", u"ｩ", u"ｪ", u"ｫ",
          u"ｯ", u"ｬ", u"ｭ", u"ｮ", u"ｳﾞ",
          u"ｶﾞ", u"ｷﾞ", u"ｸﾞ", u"ｹﾞ", u"ｺﾞ",
          u"ｻﾞ", u"ｼﾞ", u"ｽﾞ", u"ｾﾞ", u"ｿﾞ",
          u"ﾀﾞ", u"ﾁﾞ", u"ﾂﾞ", u"ﾃﾞ", u"ﾄﾞ",
          u"ﾊﾞ", u"ﾋﾞ", u"ﾌﾞ", u"ﾍﾞ", u"ﾎﾞ",
          u"ﾊﾟ", u"ﾋﾟ", u"ﾌﾟ", u"ﾍﾟ", u"ﾎﾟ",
          u"｡", u"､", u"･", u"ﾞ", u"ﾟ", u"｢", u"｣", u"ｰ"]

# maps of ascii
zh_ascii = {}
zhe_ascii = {}
hz_ascii = {}

for (z, h) in zip(z_ascii, h_ascii):
    zh_ascii[z] = h
    hz_ascii[h] = z

for (z, he) in zip(z_ascii, he_ascii):
    zhe_ascii[z] = he

del z_ascii, h_ascii, he_ascii

# maps of digit
zh_digit = {}
hz_digit = {}

for (z, h) in zip(z_digit, h_digit):
    zh_digit[z] = h
    hz_digit[h] = z

del z_digit, h_digit

# maps of KANA
zh_kana = {}
hz_kana = {}

for (z, h) in zip(z_kana, h_kana):
    zh_kana[z] = h
    hz_kana[h] = z

del z_kana, h_kana

# function check text
# argument and return: unicode string
def _check_text(t):
    if isinstance(t, UnicodeType) or t == '':
        return t
    else:
        raise zenhanError, "Sorry... You must set UNICODE String."

# function check convertion mode and make transform dictionary
# argument: integer
# return: transform dictionary
def _check_mode_zh(m):
    t_m = {}
    if isinstance(m, int) and m >= 0 and m <= 7:
        return _zh_trans_map(m)
    else:
        raise zenhanError, "Sorry... You set invalid mode."

def _check_mode_zhe(m):
    t_m = {}
    if isinstance(m, int) and m >= 0 and m <= 7:
        return _zhe_trans_map(m)
    else:
        raise zenhanError, "Sorry... You set invalid mode."

def _check_mode_hz(m):
    t_m = {}
    if isinstance(m, int) and m >= 0 and m <= 7:
        return _hz_trans_map(m)
    else:
        raise zenhanError, "Sorry... You set invalid mode."

#
def _zh_trans_map(m):
    tm = {}
    if m >=4:
        tm.update(zh_kana)
        m -= 4
    if m >= 2:
        tm.update(zh_digit)
        m -= 2
    if m:
        tm.update(zh_ascii)
    return tm

def _zhe_trans_map(m):
    tm = {}
    if m >=4:
        tm.update(zh_kana)
        m -= 4
    if m >= 2:
        tm.update(zh_digit)
        m -= 2
    if m:
        tm.update(zhe_ascii)
    return tm

def _hz_trans_map(m):
    tm = {}
    if m >=4:
        tm.update(hz_kana)
        m -= 4
    if m >= 2:
        tm.update(hz_digit)
        m -= 2
    if m:
        tm.update(hz_ascii)
    return tm


# function convert from ZENKAKU to HANKAKU
# argument and return: unicode string
def z2h(text="", mode=ALL, ignore=()):
    converted = []

    text = _check_text(text)
    zh_map = _check_mode_zh(mode)

    for c in text:
        if c in ignore:
            converted.append(c)
        else:
            converted.append(zh_map.get(c, c))

    return ''.join(converted)

def z2he(text="", mode=ALL, ignore=()):
    converted = []

    text = _check_text(text)
    zhe_map = _check_mode_zhe(mode)

    for c in text:
        if c in ignore:
            converted.append(c)
        else:
            converted.append(zhe_map.get(c, c))

    return ''.join(converted)

# function convert from HANKAKU to ZENKAKU
# argument and return: unicode string
def h2z(text, mode=ALL, ignore=()):
    converted = ['']

    text = _check_text(text)
    hz_map = _check_mode_hz(mode)

    prev = ''
    for c in text:
        if c in ignore:
            converted.append(c)
        elif c in (u"ﾞ", u"ﾟ"):
            p = converted.pop()
            converted.extend(hz_map.get(prev+c, [p, hz_map.get(c, c)]))
        else:
            converted.append(hz_map.get(c, c))

        prev = c

    return ''.join(converted)