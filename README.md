MMD Transporter
=======================
MayaでMikuMikuDanceするためのPythonプラグインです。

## 動作環境

* Windows7
* Maya2013(x64)以降
* そこそこのスペックのPC

## インストール方法

### Pythonのインストール
Mayaでは日本語を扱うことができません。
そのため、事前に日本語からローマ字に変換する必要があります。
しかし、kakasiはMaya Pythonで直接動かすことができません。
そこで、変換辞書を作成するためにコマンドラインからPythonを実行することにします。

Pythonのバージョンは2.7です。以下のリンクからインストーラをダウンロードしてください。

[Python 2.7 windows installer](https://www.python.org/download/releases/python-2.7.msi.asc)

インストール方法やパスの設定については以下のリンクを参照してください。

[Python 2.7 のインストール](http://www5f.biglobe.ne.jp/~nobml/ninix/2_python.html)


### kakasiフォルダを移動する
kakasiとは、ひらがなやカタカナ、漢字等をローマ字に変換することのできるライブラリです。MMDのモデルデータは、ボーンの名前やモーフの名前に日本語を使っているため、Mayaで読み込ませることができません。kakasiを利用することで、日本語とローマ字の変換辞書を作成します。

ZIPファイルを解凍すると、**kakasiフォルダ**が入っています。
このフォルダはプラグインの実行に必要なものです。

kakasiフォルダを**Cドライブの直下**に置いてください。
それ以外の場所に置くと実行されません。


### Human IKのルールファイルの登録
MMD Transporterで読み込んだモデルは、ルールファイルを用いることで自動的にHuman IKを設定します。そのルールファイルがMMD HumanIK.xmlです。

ルールファイルは以下のディレクトリに保存されています。

```
C:/Users/ユーザ名/AppData/Roaming/Autodesk/HIKCharacterizationTool4/Template
```

この中にMMD HumanIK.xml


## 使い方

### Pythonでmakedict.pyを実行する
mmd-transporterのフォルダ内にmakedict.pyがあります。
これは日本語とローマ字の変換辞書を作るためのスクリプトです。

まず、mmd-transporterのフォルダの上で**Shift+右クリック**を押して、「**パスとしてコピー**」を選択してください。
これでクリップボードにmmd-transporterのフォルダのパスが残りました。

次にコマンドプロンプトを開いてください。スタートメニューで「**cmd**」と検索すれば出てきます。
コマンドプロンプトが開いたら、以下のように入力してください。

```
cd (右クリック→貼り付け)
```

これでmmd-transporterのフォルダへ移動します。

コマンドプロンプトはそのままで、読み込みたいPMDもしくはPMXファイルのあるフォルダを開いてください。
PMD/PMXファイルの上で**Shift+右クリック**を押し、「パスとしてコピー」を選択します。

次に、コマンドプロンプトに戻って以下のように入力してください。

```
python makedict.py (右クリック→貼り付け)
```

これで、モデルデータのあるフォルダにいくつかのCSVファイルが書き出されました。
これは変換用の辞書ファイルなのですが、書き出したモデルにしか対応していません。
一つのフォルダの中に複数のモデルデータが入っている場合は注意してください。


### プラグインを読み込む

Plugin ManagerでMMD Transporterを登録するか、以下のコマンド（Python）を実行してプラグインとして登録してください。

```
import maya.cmds
maya.cmds.loadPlugin("mmd-transporterのパス/mmd-transporter.py")
```

### モデルデータを読み込む

モデルデータの読み込みは以下のコマンド（MEL/Python）で実行できます。

```
loadmmd
```

ダイアログが開くのでPMX/PMDを指定します。