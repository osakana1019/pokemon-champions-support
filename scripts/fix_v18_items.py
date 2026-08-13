from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Current Pokémon Champions held items for Regulation M-B.
# Cross-checked against current item lists updated through 2026-08-10.
allowed = [
    # Berries
    'クラボのみ','カゴのみ','モモンのみ','チーゴのみ','ナナシのみ','ヒメリのみ','オレンのみ','キーのみ','ラムのみ','オボンのみ',
    'オッカのみ','イトケのみ','ソクノのみ','リンドのみ','ヤチェのみ','ヨプのみ','ビアーのみ','シュカのみ','バコウのみ','ウタンのみ',
    'タンガのみ','ヨロギのみ','カシブのみ','ハバンのみ','ナモのみ','リリバのみ','ホズのみ','ロゼルのみ',
    # Battle items available in M-B
    'あついいわ','いのちのたま','おうじゃのしるし','おおきなねっこ','かいがらのすず','かたいいし','きあいのタスキ','きあいのハチマキ',
    'きせきのタネ','きれいなぬけがら','ぎんのこな','くろいてっきゅう','くろいメガネ','くろおび','こうかくレンズ','こだわりスカーフ',
    'さらさらいわ','じしゃく','しめったいわ','シルクのスカーフ','しろいハーブ','しんぴのしずく','するどいくちばし','せんせいのツメ',
    'たつじんのおび','たべのこし','ちからのハチマキ','つめたいいわ','でんきだま','どくバリ','とけないこおり','のろいのおふだ',
    'ひかりのこな','ひかりのねんど','ピントレンズ','フォーカスレンズ','まがったスプーン','メタルコート','メトロノーム','メンタルハーブ',
    'もくたん','ものしりメガネ','やわらかいすな','ようせいのハネ','りゅうのキバ'
]

js_list = '[' + ','.join('"' + x + '"' for x in allowed) + ']'
new_whitelist = (
    f'const CHAMPIONS_ITEM_RULESET="M-B / 2026-08-10";\n'
    f'const CHAMPIONS_HELD_ITEMS={js_list};\n'
    'const commonItems=CHAMPIONS_HELD_ITEMS;\n'
    'const CHAMPIONS_HELD_ITEM_SET=new Set(CHAMPIONS_HELD_ITEMS);'
)

# Replace existing v18.1 whitelist block idempotently.
pat = r'const CHAMPIONS_ITEM_RULESET="[^"]*";\nconst CHAMPIONS_HELD_ITEMS=\[[^\n]*\];\nconst commonItems=CHAMPIONS_HELD_ITEMS;\nconst CHAMPIONS_HELD_ITEM_SET=new Set\(CHAMPIONS_HELD_ITEMS\);'
if re.search(pat, s):
    s = re.sub(pat, new_whitelist, s, count=1)
else:
    pat2 = r'const CHAMPIONS_HELD_ITEMS=\[[^\n]*\];\nconst commonItems=CHAMPIONS_HELD_ITEMS;\nconst CHAMPIONS_HELD_ITEM_SET=new Set\(CHAMPIONS_HELD_ITEMS\);'
    s, n = re.subn(pat2, new_whitelist, s, count=1)
    assert n == 1, 'held-item whitelist block not found'

# Current M-B additions and common API ids -> Japanese labels.
# Prefixing duplicate object keys is harmless; later identical mappings win.
aliases = (
    '  lifeorb:"いのちのたま",expertbelt:"たつじんのおび",lightclay:"ひかりのねんど",'
    'muscleband:"ちからのハチマキ",wiseglasses:"ものしりメガネ",widelens:"こうかくレンズ",zoomlens:"フォーカスレンズ",'
    'metronome:"メトロノーム",ironball:"くろいてっきゅう",damprock:"しめったいわ",heatrock:"あついいわ",'
    'smoothrock:"さらさらいわ",icyrock:"つめたいいわ",shedshell:"きれいなぬけがら",bigroot:"おおきなねっこ",'
)
if 'lifeorb:"いのちのたま"' not in s:
    s, n = re.subn(r'(const COMMON_ENV_JA=\{\n moves:\{.*?\n \},\n items:\{\n)', r'\1' + aliases, s, count=1, flags=re.S)
    assert n == 1, 'COMMON_ENV_JA items block not found'
else:
    # Ensure every M-B alias exists even when some were previously restored.
    m = re.search(r'(const COMMON_ENV_JA=\{\n moves:\{.*?\n \},\n items:\{\n)(.*?)(\n \},\n abilities:\{)', s, re.S)
    assert m, 'COMMON_ENV_JA item block not found'
    body = m.group(2)
    wanted = {
        'lifeorb':'いのちのたま','expertbelt':'たつじんのおび','lightclay':'ひかりのねんど','muscleband':'ちからのハチマキ',
        'wiseglasses':'ものしりメガネ','widelens':'こうかくレンズ','zoomlens':'フォーカスレンズ','metronome':'メトロノーム',
        'ironball':'くろいてっきゅう','damprock':'しめったいわ','heatrock':'あついいわ','smoothrock':'さらさらいわ',
        'icyrock':'つめたいいわ','shedshell':'きれいなぬけがら','bigroot':'おおきなねっこ'
    }
    missing = ''.join(f'  {k}:"{v}",' for k,v in wanted.items() if f'{k}:"' not in body)
    if missing:
        s = s[:m.start(2)] + missing + body + s[m.end(2):]

# When rebuilding local environment DB, normalize API item ids before legality filtering.
s = s.replace(
    'items:(y.items||[]).map(x=>({name:x[0],pct:Number(x[1])||0})).filter(x=>isChampionsHeldItem(x.name)),',
    "items:(y.items||[]).map(x=>({name:x[0],pct:Number(x[1])||0})).filter(x=>isChampionsHeldItem(displayEnvTerm('items',x.name))),",
    1
)

# Restore M-B firepower item evaluation in quick-selection logic.
needle = "else if(item.includes('きあいのタスキ')){score+=2.2;itemReason='タスキで行動保証'}\n    else if(['たべのこし','オボンのみ'].some(x=>item.includes(x))){score+=1.3;itemReason='回復系持ち物で安定'}"
replacement = "else if(item.includes('きあいのタスキ')){score+=2.2;itemReason='タスキで行動保証'}\n    else if(['いのちのたま','たつじんのおび','ちからのハチマキ','ものしりメガネ'].some(x=>item.includes(x))){score+=2;itemReason='持ち物で火力を補強'}\n    else if(['たべのこし','オボンのみ'].some(x=>item.includes(x))){score+=1.3;itemReason='回復系持ち物で安定'}"
if needle in s:
    s = s.replace(needle, replacement, 1)

# Restore cleaner/endgame bonus for legal M-B offensive items if the old line was removed.
anchor = 'if(moves.some(v=>["かげうち","しんそく","ふいうち","マッハパンチ","アクアジェット","こおりのつぶて","バレットパンチ"].includes(v.name)))clean+=3;'
bonus = 'if(["いのちのたま","たつじんのおび","ちからのハチマキ","ものしりメガネ"].some(v=>item.includes(v)))clean+=2;'
if anchor in s and bonus not in s:
    s = s.replace(anchor, anchor + '\n ' + bonus, 1)

# Fix the old typo if it survives elsewhere.
s = s.replace('バリブのみ', 'リリバのみ')

# Visible version bump.
s = s.replace('Pokémon Champions Support — v18.1', 'Pokémon Champions Support — v18.2', 2)

p.write_text(s, encoding='utf-8')
print('patched current M-B held items:', len(allowed), 'ruleset=M-B / 2026-08-10')
