// 本文（生 Markdown）から読了時間を概算する。
// 日本語は「文字数 ÷ 600字/分」、欧文は「単語数 ÷ 200語/分」のハイブリッド。
// 人気の reading-time 系ライブラリは空白区切り前提で日本語を激しく過小評価するため自前で算出。

// CJK記号・約物/ひらがな/カタカナ/漢字(拡張含む)/全角形 = 日本語として数える範囲
const CJK = /[　-〿぀-ヿ㐀-䶿一-鿿＀-￯]/g;

const JP_CHARS_PER_MIN = 600;
const EN_WORDS_PER_MIN = 200;

export function readingTime(body: string | undefined): string {
  if (!body) return '1 Min Read';

  const cjkCount = (body.match(CJK) || []).length;
  const latinWords = (body.replace(CJK, ' ').match(/[A-Za-z0-9]+/g) || []).length;

  const minutes = Math.ceil(cjkCount / JP_CHARS_PER_MIN + latinWords / EN_WORDS_PER_MIN);
  return `${Math.max(1, minutes)} Min Read`;
}
