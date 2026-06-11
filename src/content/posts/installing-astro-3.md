---
title: 'Astro最高 その3'
bigTitle: 'Eidolon'
emphasis: 'Eidolon.'
headline: 'Mail from my {emphasis}'
excerpt: 'From: nilferum Subject: CI: All jobs have failed.'
author: 'nilferum'
date: 2026-06-12
cover: '/images/paper-airplane.webp'
featured: true
pageNumber: 'NO. 03'
tags: ['Astro', 'GitHub', 'CI', 'Diary']
---

サイトを立ち上げてみると、テンプレートの中に見慣れないファイルがいくつか同梱されていることに気づきます。<br>
今回はその中から`.env`と`ci.yml`、知らない子ですね……。

---

## .envってなんだ？

environmentの略？　→　あってました。

APIキーやトークンのような｢公開したくない値｣や、環境ごとに変わる値をソースにハードコードせず逃がしておくためのファイル。という理解で良さそうです。めっちゃ便利じゃん。

```astro
const Key = import.meta.env.MY_HEART_KEY_<3; //SyntaxError
```

少し調べた範囲の補足をすると、

- AstroはViteベースなので`import.meta.env`で読む
- `PUBLIC_`prefixの変数だけがクライアント側に渡され、なしの変数はサーバー/ビルド時限定。漏洩を命名規則で防ぐ安全装置になっている。
- テンプレートには最初から`.gitignore`に`.env`が入ってました。優しい。

下2つ、foolproofですね。ちなみに高校の頃の英語教師がoが2つ続いたらそこにアクセントが来る、って言ってました。

---

## ci.ymlってなんだ？

### CIってなんだ？

Continuous Integrationらしい。pushのたびに自動でビルドやチェックを走らせて、壊れたコードをmainに混ぜ込まないための仕組み。

### ymlってなんだ？

YAMLらしい。YAML Ain't a Markup Language.らしい。あーそういうことね、完全に理解した。<br>
クレタ人はいつもうそつきだし、GNUはUNIXではない。

---

## All jobs have failed

そもそもCIの存在に気づいたのは、push後に｢CI: All jobs have failed｣というメールがGitHubから届いていたからでした。

つまりpushに連動してGitHub側が何かしら実行してくれている、と推測が立ちます。ググって正確な挙動を調べてみると、<br>
リポジトリの`.github/workflows/`配下にymlを置いておくと、GitHubが気を利かせてその内容を実行してくれる仕組みが**GitHub Actions**<br>
そしてテンプレートには最初から`ci.yml`が同梱されていた、ということのようです。

取り敢えず中身を読みましょう。

```
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - uses: actions/setup-node@v6
        with:
          node-version: 22
          cache: npm

      - run: npm ci

      - name: Format check
        run: npm run format:check

      - name: Build
        run: npm run build
```

めっちゃ読みやすい**JSONの親戚**みたいなやつ来た。

で、どっかでエラーを吐いているのはわかったのですが、当然ここを読んでもどこがエラーなのかはわからないので、GitHubのエラーページに飛んで見てみましょう。

```
Run npm run format:check

> @example/self-esteem-astro@0.0.1 format:check
> prettier --check .
Checking formatting...
[warn] src/content/posts/installing-astro-1.md
[warn] src/content/posts/installing-astro-2.md
[warn] src/pages/blog/[...slug].astro
[warn] src/pages/blog/index.astro
[warn] src/pages/contact.astro
[warn] src/pages/tags/[tag].astro
[warn] Code style issues found in 6 files. Run Prettier with --write to fix.
Error: Process completed with exit code 1.
```

format:checkがエラーを吐いていました。<br>
format:check = Prettierはコードフォーマッタで、インデントや引用符、改行位置といった｢見た目の流儀｣を機械的に揃えてくれるツールらしい。<br>
`--check`は整形せずチェックだけを行い、流儀と違う箇所があると異常終了(exit code 1)を返す。そしてGitHub ActionsはAll jobs have failed.と見做す。ということだったようです。

原因はFMを囲む`---`の直後と直前に改行が入っていたこと、文字列を囲むクォーテーションマークに一箇所だけダブルが混ざっていたことでした。ご丁寧な命令文まで書いてくれていたので、おとなしくRunします。

```
npx prettier --write .
```

さて、`run: npm run build`側は実行されてなかったみたいですが、一旦これでcommitとpushしてみましょう。
**完全に解決。**

---

## 人間の尊厳を取り戻しましょう

毎回CIに怒られてから直すのも人間としての尊厳を失いかねないし、手元で揃える手段も調べておきましょう。と言っても、VSCodeにPrettier拡張があるらしいので(僕はX以外の公式マークに弱い人間です)それを入れ、Format on saveをenableすれば解決でした。

すっごい余談なんですけど、人生で初めて自分の名前からメールが届いてびっくりしました。<br>
アイコンとドメイン部を見たらすぐにGitHubからだってのはわかったんですけど、自分の幻からメールが来たような何とも言えない奇妙さを感じましたね。
