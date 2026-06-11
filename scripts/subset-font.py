"""
日本語フォント サブセット生成スクリプト

src/content 配下の md/mdx に実際に出てくる文字を収集し、
かな・ASCII・約物・全角記号の各範囲と合わせてサブセット化、woff2 で出力する。
FONTS に列挙したフォントすべてを同じ文字セットでまとめて処理する。

記事を追加して新しい漢字が出たら、このスクリプトを再実行すれば取りこぼさない。
（npm run build の prebuild フックで自動実行される）

使い方:
    python scripts/subset-font.py            # FONTS をすべて処理
    python scripts/subset-font.py 入力 出力   # 単発で1フォントだけ処理
"""

import sys
import glob
from pathlib import Path
from fontTools import subset

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "fonts-src"
OUT_DIR = ROOT / "public" / "fonts"

# 処理対象フォント (入力TTF, 出力woff2)
# 日本語本文のみセルフホスト。見出し/強調(Darker Grotesque / Bodoni Moda)は CDN。
FONTS = [
    (SRC_DIR / "ZenOldMincho-Regular.ttf", OUT_DIR / "ZenOldMincho-Subset.woff2"),
]

# 常に含める Unicode 範囲（かな・ASCII・約物・全角形など）
ALWAYS_UNICODES = ",".join([
    "U+0020-007E",   # Basic Latin
    "U+00A0-00FF",   # Latin-1 Supplement
    "U+2000-206F",   # General Punctuation（ダッシュ・引用符など）
    "U+25A0-25FF",   # 幾何学記号（■● など本文で使う飾り）
    "U+3000-303F",   # CJK 記号と約物（、。「」など）
    "U+3040-309F",   # ひらがな
    "U+30A0-30FF",   # カタカナ
    "U+31F0-31FF",   # カタカナ拡張
    "U+FF00-FFEF",   # 半角・全角形（！？（）など）
])


def collect_text_chars() -> str:
    """src 配下の md/mdx から使用文字を集める。"""
    chars = set()
    for pattern in ("src/content/**/*.md", "src/content/**/*.mdx"):
        for path in glob.glob(str(ROOT / pattern), recursive=True):
            chars.update(Path(path).read_text(encoding="utf-8"))
    return "".join(sorted(chars))


def make_subset(src: str, out: str, text: str) -> None:
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    subset.main([
        src,
        f"--text={text}",
        f"--unicodes={ALWAYS_UNICODES}",
        "--layout-features=palt,kern,liga,vert,vrt2",
        "--flavor=woff2",
        f"--output-file={out}",
    ])
    size_kb = Path(out).stat().st_size / 1024
    print(f"[subset] {Path(src).name} -> {Path(out).name}  ({size_kb:,.1f} KB)")


def main():
    text = collect_text_chars()
    print(f"[subset] content chars collected: {len(set(text))}")

    if len(sys.argv) > 2:
        # 単発モード（1フォントだけ）
        make_subset(sys.argv[1], sys.argv[2], text)
        return

    for src, out in FONTS:
        if not Path(src).exists():
            print(f"[subset] SKIP (missing): {src}")
            continue
        make_subset(str(src), str(out), text)


if __name__ == "__main__":
    main()
