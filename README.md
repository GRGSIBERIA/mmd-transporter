MMD Transporter
=======================
MayaでMikuMikuDanceするためのPythonプラグインです。

# インストール方法


## kakasiフォルダを移動する
kakasiとは、ひらがなやカタカナ、漢字等をローマ字に変換することのできるライブラリです。MMDのモデルデータは、ボーンの名前やモーフの名前に日本語を使っているため、Mayaで読み込ませることができません。kakasiを利用することで、日本語とローマ字の変換辞書を作成します。

ZIPファイルを解凍すると、**kakasiフォルダ**が入っています。
このフォルダはプラグインの実行に必要なものです。

kakasiフォルダを**Cドライブの直下**に置いてください。
それ以外の場所に置くと実行されません。


## Pythonのインストール
kakasiはMaya Pythonで直接動かすことができません。
そこで、変換辞書を作成するためにコマンドラインからPythonを実行することにします。

Pythonのバージョンは2.7です。以下のリンクからインストーラをダウンロードしてください。

[Python 2.7 windows installer](https://www.python.org/download/releases/python-2.7.msi.asc)

インストール方法やパスの設定については以下のリンクを参照してください。

[Python 2.7 のインストール](http://www5f.biglobe.ne.jp/~nobml/ninix/2_python.html)

