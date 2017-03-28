# -*- coding: utf-8 -*-

from . import _Converter

class Converter(_Converter):
    def __init__(self):
        self.z_ascii = (
            u"ａ", u"ｂ", u"ｃ", u"ｄ", u"ｅ", u"ｆ", u"ｇ", u"ｈ", u"ｉ",
            u"ｊ", u"ｋ", u"ｌ", u"ｍ", u"ｎ", u"ｏ", u"ｐ", u"ｑ", u"ｒ",
            u"ｓ", u"ｔ", u"ｕ", u"ｖ", u"ｗ", u"ｘ", u"ｙ", u"ｚ",
            u"Ａ", u"Ｂ", u"Ｃ", u"Ｄ", u"Ｅ", u"Ｆ", u"Ｇ", u"Ｈ", u"Ｉ",
            u"Ｊ", u"Ｋ", u"Ｌ", u"Ｍ", u"Ｎ", u"Ｏ", u"Ｐ", u"Ｑ", u"Ｒ",
            u"Ｓ", u"Ｔ", u"Ｕ", u"Ｖ", u"Ｗ", u"Ｘ", u"Ｙ", u"Ｚ",
            u"！", u"”", u"＃", u"＄", u"％", u"＆", u"’", u"（", u"）",
            u"＊", u"＋", u"，", u"−", u"．", u"／", u"：", u"；", u"＜",
            u"＝", u"＞", u"？", u"＠", u"［", u"￥", u"］", u"＾", u"＿",
            u"‘", u"｛", u"｜", u"｝", u"〜", u"　")

        self.z_digit = (
            u"０", u"１", u"２", u"３", u"４",
            u"５", u"６", u"７", u"８", u"９")

        self.z_kana = (u"ア", u"イ", u"ウ", u"エ", u"オ",
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
                       u"。", u"、", u"・", u"゛", u"゜", u"「", u"」", u"ー")

        self.h_ascii = (
            u"a", u"b", u"c", u"d", u"e", u"f", u"g", u"h", u"i",
            u"j", u"k", u"l", u"m", u"n", u"o", u"p", u"q", u"r",
            u"s", u"t", u"u", u"v", u"w", u"x", u"y", u"z",
            u"A", u"B", u"C", u"D", u"E", u"F", u"G", u"H", u"I",
            u"J", u"K", u"L", u"M", u"N", u"O", u"P", u"Q", u"R",
            u"S", u"T", u"U", u"V", u"W", u"X", u"Y", u"Z",
            u"!", u'"', u"#", u"$", u"%", u"&", u"'", u"(", u")",
            u"*", u"+", u",", u"-", u".", u"/", u":", u";", u"<",
            u"=", u">", u"?", u"@", u"[", u"\\", u"]", u"^", u"_",
            u"`", u"{", u"|", u"}", u"~", u" ")

        self.h_digit = (
            u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9")

        self.h_kana = (u"ｱ", u"ｲ", u"ｳ", u"ｴ", u"ｵ",
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
                       u"｡", u"､", u"･", u"ﾞ", u"ﾟ", u"｢", u"｣", u"ｰ")

        super(Converter, self).__init__()

    def zen2han(self, text, mode, ignore):
        if isinstance(text, unicode) or text == '':
            pass
        else:
            raise TypeError('You must set unicode string')

        if self._is_valid_mode(mode):
            zh_dict = self._make_zen2han_dict(mode)
        else:
            raise ValueError('Invalid mode value')

        converted = []
        for c in text:
            if c in ignore:
                converted.append(c)
            else:
                converted.append(zh_dict.get(c, c))

        return u''.join(converted)

    def han2zen(self, text, mode, ignore):
        if isinstance(text, unicode) or text == '':
            pass
        else:
            raise TypeError('You must set unicode string')

        if self._is_valid_mode(mode):
            hz_dict = self._make_han2zen_dict(mode)
        else:
            raise ValueError('Invalid mode value')

        converted = [u'']
        prev = u''
        for c in text:
            if c in ignore:
                converted.append(c)
            elif c in (u"ﾞ", u"ﾟ"):
                p = converted.pop()
                converted.extend(hz_dict.get(prev+c, [p, hz_dict.get(c, c)]))
            else:
                converted.append(hz_dict.get(c, c))
            prev = c

        return u''.join(converted)
