MMD Transporter
=======================
MayaでMikuMikuDanceするためのPythonプラグインです。


## 動作環境

* Windows7 64bit(推奨)
* Maya2016(x64)以降
* そこそこのスペックのPC


## 実装されているコマンド・機能

* loadmmd
  - PMD/PMXファイルの読み込み
  - メッシュの構築
  - マテリアルの構築/適用
  - ボーン/スキニングの設定/適用
  - BlendShapeの設定/適用
  - Human IKのテンプレートの同梱
  - Maya Bulletの適用
* mmdbswindow
  - BlendShapeの一覧化
  - BlendShape名の日本語表示
  - 対象BlendShapeのキーフレームの追加/削除



## インストール方法

### MeCabのインストール
MMD Transporterでは，MeCabで日本語文字列を英語に仮変換します．

install.batを**管理者権限で実行**するとMeCabのインストールが始まります．
使用する辞書は，**UTF-8を指定してください**．



### Human IKプラグインの初期化
既にHuman IKを利用したことがある場合は飛ばして下さい．

Human IKのプラグインを読み込み，ユーザフォルダのAppDataにHuman IK用の設定フォルダを生成します．

[Window]-[Settings/Preferences]-[Plug-in Manager]でプラグイン・マネージャを開いてください．
その中に，**mayaHIK.mll**があります．
mayaHIK.mllのloadedとauto loadにチェックを入れてHuman IKプラグインを読み込んでください．

次に，Human IKを起動します．
[Animation]-[Skeleton]-[HumanIK...]を選択します．
Character Controllというドックが新しく作成されますので，
その中から[Create]-[Skeleton]ボタンをクリックします．

これにより，```ユーザフォルダ/AppData/Roaming/Autodesk/HIKCharacterizationTool4```というフォルダが作成されます．
Human IKの初回起動時の設定は以上です．



### Bulletプラグインを有効化する
MMDでは物理演算にBulletを利用しています。
MMD Transporterもそれに習い、Bulletプラグインを利用してMMDの物理演算を再現します。

[Window]-[Settings/Preferences]-[Plug-in Manager]でPlug-in Managerを開いてください。その中に、**bullet.mll**という項目がありますので、LoadedとAuto loadの両方をチェックしてください。

たまに起動時にBulletのプラグインがIndex Out of Range（値が範囲外です）で落ちることがあります。Bulletを扱う上ではそこまで問題にならないと思うのですが、気になる場合は読み直してみてください。



## 使い方

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

ダイアログが開くのでPMX/PMDを指定します。今のところPMXの読み込みのみ対応しています。UVモーフ、ボーンモーフが設定されているモデルは未対応です。


### HumanIKの使い方
Human IKとは、Mayaのプラグインの一つです。利点は色々あるのですが、その中でもボーンの共通規格からFull Body IK（FBIK）とリグを自動的に構築できるという点です。FBIKとは、体全体を引っ張るように操作できるIKのことです。

Human IKは[Skeleton]-[Human IK]でペインが生成されます。Character ControlsのDefineからCreateを押すと、Human IKのキャラクターが生成されます。

まず、Human IKで最初にやることは、Defineで各種コントローラの部位とボーンを対応付けることです。MMD Transporterでは、テンプレートを事前に用意してあるため、このテンプレートを読み込むと、自動的に登録が完了します。

読み込んだモデルデータの**ルートボーンを選択し、Select Hierarchyで全てのボーンを選択してある状態**にしてください。

その次にペイン上部のアイコン(Load Skeleton Definition)を押し、TemplateからMMD HumanIKを選んでください。ラジオボタンが二つありますが、そのうち下にあるMatch only selected bonesを選択してください。これでOKボタンを押すと自動的にHuman IKが適用されます。

ただし、MMDではAスタンスが基本となっているため、Human IKの設定は完全に適用されません。腕を水平にすればスケルトンの定義をロックできるようになるので、**肩や鎖骨等を弄って全部緑になるように、ボーンの回転角を調整してください**。腕を水平にするのは肩の構造上あまりよろしくないため不具合が残る可能性があります。


### MMD Transporter専用Blend Shape Editor
MMD Transporterでは、日本語を一度ローマ字にしています。これは、Mayaがオブジェクトの名前に英語しか扱えない制約があるためです。そのため、Maya付属のBlend Shape Editorでは、Blend Shape名が全てローマ字になってしまい、たいへん使いづらいです。

そこで、BlendShape用の専用のエディタを作成しました。使い方はBlend Shape Editorとだいたい同じです。MMD Transporterで変換したモデル（transform）を選択し、以下のコマンドを実行することでエディタを呼び出します。




## よくある質問

### 顔の裏側が見える，透明なオブジェクトのレンダリングが変

Maya 2016では，デフォルトの設定で透明なオブジェクトを簡易的に表示しています．
Maya 2016以前では，カメラの[Shading]-[Polygon Transparency Sorting]で正しく描画することができます．
Maya 2016からViewport 2.0が導入されてオプションの位置が変わりました．

カメラの[Renderer]-[Viewport 2.0]のオプションから[Hardware Renderer 2.0 Settings]を開きます．
[Performance]パネルから，[Transparency Algorithm]-[Depth Peeling]を選択し，[Transparency Quality]を1.0に設定します．
これで，透明なオブジェクトも正常にレンダリングされるようになります．





## お借りしたもの

* [MeCab](http://taku910.github.io/mecab/)
  - 京都大学情報学研究科−日本電信電話株式会社コミュニケーション科学基礎研究所 共同研究ユニットプロジェクト
  - BSDライセンス
* [pymeshio](https://github.com/ousttrue/pymeshio)
  - ousttrue
  - zlib/png 1.0 
* [MeCab 0.98 野良ビルド](http://d.hatena.ne.jp/fgshun/20090910/1252571625)
  - fgshun
* [zenhan-py](https://github.com/MiCHiLU/zenhan-py)
  - ENDOH takanao

## ライセンス

GNU GENERAL PUBLIC LICENSE Version 2


## 謝辞

本プロジェクトは独立行政法人情報処理推進機構(IPA)の未踏IT人材発掘・育成事業の支援を受けて開発されています。


## Copyright

Eiichi Takebuchi(GRGSIBERIA)