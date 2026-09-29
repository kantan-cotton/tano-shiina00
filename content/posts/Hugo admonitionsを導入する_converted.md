---
categories:
  - Web制作
class:
type:
genre:
feature:
title: Calloutsが使えるようになるHugo admonitionsを導入する
author:
aliases:
source:
description: HugoでObsidianのCallouts記法を使うために、KKKZOZ氏が作成したHugo admonitionsを導入する
created: 2026-09-29 09:18:38
modified: 2026-09-29 11:17:19
slug: wepvf6x7
images:
  - /images/ogp/wepvf6x7.png
date: 2026-09-29T21:18:38+09:00
tags:
  - Obisidian
  - Hugo
weight:
draft: false
---

# Hugo admonitionsを導入する

## 前書き

- Hugoでは[Render hooks](https://gohugo.io/render-hooks/blockquotes/#alerts)を利用してObisidianのCallouts記法をそのまま採用できる。  
- この機能はデフォルトでONになっているわけではなく、使用者が自分で対応する必要がある。  
- もしくは有志が作成したHugo-admonitionsというモジュールを使う手もある。今回はこちらを選択した。  
- Hugo-admonitionsには豊富な`[!TIP]`や`[!CAUTION]`だけでなく、`[!TASK]`や`[!CODE]`など、21種類のCalloutsに対応している。詳しくは作者であるKKKZOZ氏の[GitHub](https://github.com/KKKZOZ/hugo-admonitions)をチェック。
- Multi-language SupportにJapaneseは含まれていないが、今のところ問題はなさそう。

## Hugo-admonitionsをGit submoduleとしてインストールする

> [!INFO]
> - Hugoのバージョン：v0.166+extend
> - Hugoで使用しているテーマ：PaperMod
> - テーマとしてではなくGit submoduleとしてインストールする理由は以下
> 	- テーマやモジュールをサイト本体のリポジトリにコピーせず、それぞれのバージョンをGitで管理しやすくするため

1. 使っているHugoサイトのルートディレクトリで、Powershellなどから`git submodule add --depth 1 https://github.com/KKKZOZ/hugo-admonitions.git themes/hugo-admonitions`を実行
2. `git submodule status`でHugo-admonitionsがsubmoduleとして登録され、コミットIDが表示されていることを確認
3. 適当なテキストエディタでhugo.tomlを開き、使用しているテーマを記入している箇所にhugo-admonitionsを追加。たとえば、theme = 'PaperMod' であれば、その行を theme = ['hugo-admonitions', 'PaperMod'] に差し替える（hugo-admonitionsが、使用しているテーマよりも必ず先＝左側に来るようにする）。
4. ローカルでCalloutsが動作していることを確認したら、変更をgit addしてcommitしてpush

　これでおそらくコールアウトがHugoでも使えるようになるはず。

## Calloutsの開閉がうまく機能しない

- ObsidianのCalloutsでは`[!TIP]+`や`[!INFO]-`のようにして、コールアウトが「デフォルトで展開した状態にするか、折りたたんだ状態にするか」を制御できる。
- hugo-admonitionsのGitHubにも、Foldable Admonitionsとして紹介されているのだが、自分の環境では+-どちらを置いても閉じたままで表示されてしまった。
- おま環か仕様かは不明（たしかにGitHubの当該箇所にあるサンプル画像をみると、+と-のどちらでもコールアウトは閉じている）。

### 対策

- コールアウトに`+`がつけられている場合だけ、デフォルトで展開した状態にするように指定する。
- Hugoではサイト側のレイアウトに同名のファイルを置くことで、テーマ側のテンプレートを上書きできる。

1. `themes\hugo-admonitions\layouts\_default\_markup`にある、render-blockquote-alert.htmlを、サイト側の`layouts/_default/_markup/`にコピー
2. コピーした方のrender-blockquote-alert.htmlをテキストエディタで開いて、`<details class="admonition {{ $type }}">`を、`<details class="admonition {{ $type }}"{{ if eq .AlertSign "+" }} open{{ end }}>`に変更
3. ローカルでCalloutsの開閉が動作していることを確認したら、変更をgit addしてcommitしてpush

> [!SUCCESS]+ デフォルトでOpenにできました🎊
> やったね🎉