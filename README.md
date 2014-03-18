# MMD Transporter

MMDのモデルデータをMayaに持ってくるためのプラグインです．ただし，PMD/PMXを直接インポートするプラグインではないのであしからず．

現在サポートしているのは以下の機能です．

* CSV読み込み
  * ポリゴン
  * 材質
  * テクスチャ
  * ボーン

### 使い方
PMX Editorで読み込んだモデルデータをCSVで書き出してください（[ファイル]-[テキスト(CSV)変換]-[CSVファイルへ出力]）．CSVはモデルデータと同じ場所に保存してください．

ソースコードをダウンロードしたら以下のコードをScript Editorで実行するか，
もしくはMMD TransporterをPlug-in Managerから読み込んでください．

```python:script.py
# Script Editorから実行する場合は必ずMMD Transporterを保存したパスを指定してください
import maya.cmds
maya.cmds.loadPlugin("/mmd-transporterのパス/main.py")
```

コマンドラインもしくはScript Editorでloadmmdを実行すると，ファイル選択ダイアログが表示されます．最初に保存したCSVを指定してください．この時，何か言われますが無視してYesをクリックしてください．

しばらく待つとロードが完了します．

### Q&A
---------------------------------
#### モデルの表示がおかしい
カメラメニューの[Shading]-[Polygon Transparency Sorting]と[Shading]-[Object Transparency Sorting]をオンにしてください．