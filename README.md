# MMD Transporter

MMDのモデルデータをMayaに持ってくるためのプラグインです．ただし，PMD/PMXを直接インポートするプラグインではないのであしからず．

現在サポートしているのは以下の機能です．

* CSV読み込み
  * ポリゴン
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

PMX EditorでCSVに変換されているモデルデータを読み込みます．

#### -m(-mesh)フラグ
このフラグをオンにすると，CSVからメッシュのみ読み込みます．

#### -mt(-material)フラグ
このフラグをオンにすると，マテリアルの読み込みまで行います．

#### -fm(-faceMaterial)フラグ
このフラグをオンにすると，メッシュに対してマテリアルの適用まで行います．

#### -b(-bone)フラグ
このフラグをオンにすると，ボーンの配置まで行います．

#### -s(-skinning)フラグ
このフラグをオンにすると，読み込んだメッシュとボーンについてスキニングまで行います．

#### -w(-weight)フラグ
このフラグをオンにすると，ウェイトの設定まで行います．


## Copyright
Copyright (c) Eiichi Takebuchi, released under the MIT license.