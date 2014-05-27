MMD Transporter
=======================
MayaでMikuMikuDanceするためのPythonプラグインです。


## 動作環境

* Windows7 64bit(推奨)
* Python 2.7
* Maya2014(x64)以降
* そこそこのスペックのPC


## 実装されている機能

* loadmmd
  - PMD/PMXファイルの読み込み
  - メッシュの構築
  - マテリアルの構築/適用
  - ボーン/スキニングの設定/適用
  - BlendShapeの設定/適用
  - Human IKのテンプレートの同梱
  - Maya Bulletの適用
* mmdbswindow
  - BlendShape用ツール


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


### インストールフォルダでinstall.pyを実行する
MMD Transporterの中に、install.pyというファイルが存在します。
このファイルはMMD Transporterのインストールをするためのファイルです。

MMD Transporterをインストールしたい場所へ移したら、install.pyを実行してください。Pythonがインストールされている状態であれば、ダブルクリックでも実行できます。できれば、管理者権限での実行がいいです。

**Installing Failedと表示されなければ大丈夫です。**

### Bulletプラグインを有効化する
MMDでは物理演算にBulletを利用しています。
MMD Transporterもそれに習い、Bulletプラグインを利用してMMDの物理演算を再現します。

[Window]-[Settings/Preferences]-[Plug-in Manager]でPlug-in Managerを開いてください。その中に、**bullet.mll**という項目がありますので、LoadedとAuto loadの両方をチェックしてください。

さがすのが面倒くさい場合は、以下のMELでbullet.mllを読み込むことができます。

```
loadPlugin "bullet"
```

たまに起動時にBulletのプラグインがIndex Out of Range（値が範囲外です）で落ちることがあります。Bulletを扱う上ではそこまで問題にならないと思うのですが、気になる場合は読みなおしてみてください。


### Human IKのテンプレートの登録
** install.pyを実行すると自動的に登録が行われますが、たまに失敗することがあります。以下の手順は手動で登録を行う方法です。 **

MMD Transporterで読み込んだモデルは、テンプレートを用いることで自動的にHuman IKを設定します。そのテンプレートがMMD HumanIK.xmlです。

テンプレートは以下のディレクトリに保存されています。

```
C:/Users/ユーザ名/AppData/Roaming/Autodesk/HIKCharacterizationTool4/template
```

この中にMMD HumanIK.xmlを入れてください。もし見つからない場合は以下の手順でテンプレートを入れることができます。

1. Mayaを起動する
2. 適当にスケルトンを置く
3. [Skeleton]-[Human IK]を選択
4. Character ControlsのDefineからSkeletonを選択
5. 適当に置いたスケルトンを選択
6. Character Controlsの上部のアイコン(Load Skeleton Definition)をクリック
7. Templateのプルダウンメニューから[Browse]を選択
8. MMD HumanIK.xmlのファイルをコピーする
9. 7番で表示されたダイアログで右クリックを押して貼り付け

当該ディレクトリにテンプレートが保存されると、Load Skeleton DefinitionのTemplateにMMD HumanIKが追加されます。


## 使い方

### 辞書ファイルを作成する
install.pyが実行され、インストールが正常に終わると、
makedict.batというファイルがMMD Transporterの中に作成されます。
このファイルにドラッグ＆ドロップでPMD/PMX等のモデルデータを投げると、
モデルデータが入っているディレクトリに、自動的に辞書ファイルが作成されます。


### プラグインを読み込む

Plugin ManagerでMMD Transporterを登録するか、以下のコマンド（Python）を実行してプラグインとして登録してください。

```
import maya.cmds
maya.cmds.loadPlugin("mmd-transporterのパス/lib/mmd-transporter.py")
```

Plugin Managerでは、LoadのほかにAuto Loadにもチェックを入れると、プラグインを読み込む操作が省けて便利です。

### モデルデータを読み込む

モデルデータの読み込みは以下のコマンド（MEL/Python）で実行できます。

```
maya.cmds.loadmmd()
```

ダイアログが開くのでPMX/PMDを指定します。


### 顔の裏側や不自然に描画される等の問題を解決する
MMDの透過テクスチャの描画順は材質順に準拠しています。一方で、MayaではZソートで描画順を決めています。この違いにより、シェーディングをTexturedの状態にすると表示が崩れてしまいます。

表示が崩れてしまった場合は、カメラのパネルで[Shading]-[Polygon Transparency Sorting]をオンにするとある程度は正常に描画されるようになります。


### HumanIKの設定
Human IKとは、Mayaのプラグインの一つです。利点は色々あるのですが、その中でもボーンの共通規格からFull Body IK（FBIK）をとリグを自動的に構築できるという点です。FBIKとは、体全体を引っ張るように操作できるIKのことです。

Human IKは[Skeleton]-[Human IK]でペインが生成されます。Character ControlsのDefineからCreateを押すと、Human IKのキャラクターが生成されます。

まず、Human IKで最初にやることは、Defineで各種コントローラの部位とボーンを対応付けることです。MMD Transporterでは、テンプレートを事前に用意してあるため、このテンプレートを読み込むと、自動的に登録が完了します。

読み込んだモデルデータの**ルートボーンを選択して、Select Hierarchyで全てのボーンを選択してある状態**にしてください。

その次にペイン上部のアイコン(Load Skeleton Definition)を押し、TemplateからMMD HumanIKを選んでください。ラジオボタンが二つありますが、そのうち下にあるMatch only selected bonesを選択してください。これでOKボタンを押すと自動的にHuman IKが適用されます。

ただし、MMDではAスタンスが基本となっているため、Human IKの設定は完全に適用されません。腕を水平にすればスケルトンの定義をロックできるようになるので、**肩や鎖骨等を弄って全部緑になるように、ボーンの回転角を調整してください**。腕を水平にするのは肩の構造上あまりよろしくないため不具合が残る可能性があります。


### MMD Transporter専用Blend Shape Editor
MMD Transporterでは、日本語を一度ローマ字にしています。これは、Mayaがオブジェクトの名前に英語しか扱えない制約があるためです。そのため、Maya付属のBlend Shape Editorでは、Blend Shape名が全てローマ字になってしまい、たいへん使いづらいです。

そこで、BlendShape用の専用のエディタを作成しました。使い方はBlend Shape Editorと同じです。MMD Transporterで変換したモデルデータを選択し、以下のコマンドを実行することでエディタを呼び出します。

```
maya.cmds.mmdbswindow()
```


## お借りしたもの

* [KAKASI - 漢字→かな(ローマ字)変換プログラム](http://kakasi.namazu.org/)
* [pymeshio](https://github.com/ousttrue/pymeshio)

## ライセンス

GNU GENERAL PUBLIC LICENSE Version 2

## Copyright

Eiichi Takebuchi(GRGSIBERIA)