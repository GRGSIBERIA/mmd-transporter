# MMD Transporter

MMDのモデルデータをMayaに持ってくるためのプラグインです．ただし，PMD/PMXを直接インポートするプラグインではないのであしからず．

現在サポートしているのは以下の機能です．

* CSV読み込み
  * メッシュ
  * 材質
  * テクスチャ
  * ボーン
  * スキニング

## 動作環境
* PMX Editor v0.2.2.0b
* Maya 2014(学生版)

## 使い方
PMX Editorで読み込んだモデルデータをCSVで書き出してください（[ファイル]-[テキスト(CSV)変換]-[CSVファイルへ出力]）．CSVはモデルデータと同じ場所に保存してください．

ソースコードをダウンロードしたら以下のコードをScript Editorで実行するか，
もしくはMMD TransporterをPlug-in Managerから読み込んでください．

```MEL:script.mel
#MELの場合
loadPlugin "mmd-transporterのパス/main.py"
```

```python:script.py
#Pythonの場合
import maya.cmds
maya.cmds.loadPlugin("mmd-transporterのパス/main.py")
```

コマンドラインかScript Editorで__loadmmd__を実行すると，ファイル選択ダイアログが表示されます．最初に保存したCSVを指定してください．この時，何か言われますが無視してYesをクリックしてください．

しばらく待つとロードが完了します．

モデルの表示がおかしい場合，カメラメニューの[Shading]-[Polygon Transparency Sorting]と[Shading]-[Object Transparency Sorting]をオンにしてください．

### 動作テストモデル
* Tda式初音ミク・アペンドver1.0


## コマンドマニュアル

### loadmmd

    loadmmd (-m|-mt|-fm|-b|-s|-w)

PMX EditorでCSVに変換されているモデルデータを読み込みます．モデルデータの読み込みは下記のような順番で行われます．

1. メッシュの読み込み
2. マテリアルの読み込み
3. メッシュに対してマテリアルの適用
4. ボーンの配置
5. メッシュとボーンに対してSmooth Bindを行う
6. メッシュのウェイトを設定する

各種フラグ(-m，-mt，-fm，-b，-s，-w)はそれぞれの読み込みの順番と対応しています．
これらのフラグを設定することで，そのフラグが設定されているところまでモデルデータを読み込むことができます．

#### -m(-mesh)フラグ
このフラグをオンにすると，CSVからメッシュのみ読み込みます．
-mt，-fm，-b，-s，-wとの併用はできません．

#### -mt(-material)フラグ
このフラグをオンにすると，マテリアルの読み込みまで行います．
-m，-fm，-b，-s，-wとの併用はできません．

#### -fm(-faceMaterial)フラグ
このフラグをオンにすると，メッシュに対してマテリアルの適用まで行います．
-m，-mt，-b，-s，-wとの併用はできません．

#### -b(-bone)フラグ
このフラグをオンにすると，ボーンの配置まで行います．
-m，-mt，-fm，-s，-wとの併用はできません．

#### -s(-skinning)フラグ
このフラグをオンにすると，読み込んだメッシュとボーンについてスキニングまで行います．
-m，-mt，-fm，-b，-wとの併用はできません．

#### -w(-weight)フラグ
このフラグをオンにすると，ウェイトの設定まで行います．
-m，-mt，-fm，-b，-sとの併用はできません．

## Copyright
Copyright (c) Eiichi Takebuchi, released under the MIT license.