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

mecabフォルダの中には，4つのファイルが入っています．

* _MeCab.pyd
* MeCab.py
* libmecab-1.dll
* mecab-0.996.exe

まずは，**mecab-0.996.exe**をクリックして，MeCabをインストールしてください．
使用する辞書は，**UTF-8を指定してください**．

次は，残りの3つのファイル（_MeCab.pyd，MeCab.py，libmecab-1.dll）を，以下のフォルダにコピー＆ペーストしてください．

```
Maya2016のインストールフォルダ/Python/Lib/site-packages
```

これでMeCabのインストールは終了です．

## お借りしたもの

* [MeCab](http://taku910.github.io/mecab/)
  - 京都大学情報学研究科−日本電信電話株式会社コミュニケーション科学基礎研究所 共同研究ユニットプロジェクト
  - BSDライセンス
* [pymeshio](https://github.com/ousttrue/pymeshio)
  - ousttrue
  - zlib/png 1.0 
* [MeCab 0.98 野良ビルド](http://d.hatena.ne.jp/fgshun/20090910/1252571625)
  - fgshun
* [zenhan 0.5](https://pypi.python.org/pypi/zenhan)
  - SETOGUCHI Mitsuhiro
  - MITライセンス

## ライセンス

GNU GENERAL PUBLIC LICENSE Version 2


## 謝辞

本プロジェクトは独立行政法人情報処理推進機構(IPA)の未踏IT人材発掘・育成事業の支援を受けて開発されています。


## Copyright

Eiichi Takebuchi(GRGSIBERIA)