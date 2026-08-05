---
title: 'Figiyama Gangsta Paradise'
bigTitle: 'Figiyama'
emphasis: 'Figiyama'
headline: '{emphasis} Gangsta Paradise'
excerpt: 'What is this? Absolutely atrocious... Have you ever stopped to consider what it would feel like to be shot with a line like this?'
author: 'nilferum'
date: 2026-07-14
cover: '/images/inverted-fuji.webp'
featured: true
pageNumber: 'NO. 04'
tags: ['Figma', 'CSS', 'Design']
---

たまにFigmaのBorderが消えることがあって疑問があった。<br>
再現性が不明だったが、有力な仮説を思いついた。今のところこの現象として説明可能だと思われるため備忘録を残しておく。

---

## Vocabulary

日本語では｢リセットCSS｣という表記を(体感ベースでは)よく見るが、当たった文献では英語だと`this global css reset is...`や単純に`-- styles are reset`のように後置修飾されることも多かった。(Wikipedia.enの独立記事ではReset Style Sheet)<br>
ページ内検索用に本記事では｢CSSリセット｣と記す。

~~そもそも全称セレクタではCascadedというよりすべてのセレクタに逐次適用しているのだから個別プロパティでの言及ではC抜きにするのが正しいのでは？ ボブは訝しんだ~~

---

## CSS Border vs Figma Border

### CSS

自分はCSSリセットとして[Andy Bell氏のA (more) Modern CSS Reset](https://piccalil.li/blog/a-more-modern-css-reset/)を使用している。

```css
/* Box sizing rules */
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

`box-sizing` の値はcontent-box(initial)/border-boxの二値を取る。<br>
参考: [box-sizing - CSS | MDN](https://developer.mozilla.org/ja/docs/Web/CSS/Reference/Properties/box-sizing)

CSSのbox sizing modelは歴史的にはcontent-boxがデフォルト(=initialとして設定されている)のだが、デファクトスタンダードとしてはborder-boxが採用されている。

余談だが、理由を調べてみると皮肉なことに、暴虐非道なIEの仕様がborder-box相当の振る舞いをしていたらしく、それが後年に標準化して運用されているらしい。実際、[BootstrapのReboot](https://github.com/twbs/bootstrap/issues/12351)や[TailwindのPreflight](https://tailwindcss.com/docs/preflight)といった各種フレームワークのCSSリセットでも採用されている。

端的に言えばCSS Borderは概ね`border-box;`が適用されており、borderをwidth/heightに**含む**挙動を無意識に期待している。

なお、あまり意識しづらい箇所だが、borderの真下も一応background-colorは適用されているらしい。<br>
border自体の色を半透明にしたり、pseudo要素を敢えて辺の長さより短く配置してinsetのうち任意の値2つを0として与えたり、dashのborderを与えればわかりやすい。<br>
参考: [background-clip - CSS | MDN](https://developer.mozilla.org/ja/docs/Web/CSS/Reference/Properties/background-clip)

### Figma

他方、Figmaでは`線/位置: 内側`が初期値だった。<br>
であるならば、塗りによって描写される矩形の下側に線が入り込んでいるのでは? と推測した。

しかしながらこれは最も一般的なパターンに適用されない。何も考えずにFigmaで矩形のフレームを作り、塗りと線を与えてもその線自体は可視状態。<br>
なんらかの条件付きで**線**が**他の何か**に遮蔽されている、と考えるのが妥当。

思い出してみると、この線が隠れる現象はそのフレームが子を持つ時に発生している。より正確に均すと、block/inline方向(もしくは両方)の`padding: 0;`であるときに発生していた。

つまるところ、｢Figmaはboxの内部にborderを持ちたがる｣ことと｢子の要素が親の要素より上に描画される｣という2つの性質が、親のborderより子backgroundが上に来るという奇妙な現象を引き起こしていた。文字にすると余計ややこしいですね……。

---

## Conclusion

```
線が消えた場合
子を持つ? -yes-> 子は塗りを持つ? -yes-> 線の位置を外側にすれば解決。
```

~~極めて遺憾ながらnoについて一切言及がないバカみたいな~~結論に至ることになった。

ただデザインを行なう場合、FigmaとCSSの対応関係の衝突については意識しづらい上、デザイントークン作成の段階では(variantで色を変更する場合など)、CSS側では省略できる塗りを、Figma側では明示化を兼ねて設定しておきたい箇所もある。<br>
そのような場合にドツボにハマりやすく、レンダリング側の問題なのか不明瞭なケースも多いと感じたため、誰かにLong-tailのtailになればいいなと思って残しておきます。

余談ながら、こんなところでも小学生の頃に起きたブラウザ戦争の話が出てくるのが、自分たちは歴史の中に生きてるんだという奇妙な感慨に浸る機会を与えてくれました。韓国にInternet Explorerの墓があるらしいので今度旅行の際には墓参りに行ってみようと思います。<br>
"He was a good tool to download other browsers"って言いますし、`winget`が生まれた現在、Edgeよりも少なくとも偉い。
