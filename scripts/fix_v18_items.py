from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

allowed = [
    'きあいのタスキ','こだわりスカーフ','オボンのみ','ラムのみ','たべのこし','メンタルハーブ','しろいハーブ',
    'せんせいのツメ','おうじゃのしるし','ピントレンズ','ひかりのこな','きあいのハチマキ','かいがらのすず',
    'もくたん','しんぴのしずく','きせきのタネ','じしゃく','とけないこおり','くろおび','どくバリ','やわらかいすな',
    'するどいくちばし','まがったスプーン','ぎんのこな','かたいいし','のろいのおふだ','りゅうのキバ','くろいメガネ',
    'メタルコート','ようせいのハネ','シルクのスカーフ','でんきだま',
    'クラボのみ','カゴのみ','モモンのみ','チーゴのみ','ナナシのみ','ヒメリのみ','オレンのみ','キーのみ',
    'ホズのみ','オッカのみ','イトケのみ','ソクノのみ','リンドのみ','ヤチェのみ','ヨプのみ','ビアーのみ','シュカのみ',
    'バコウのみ','ウタンのみ','タンガのみ','ヨロギのみ','カシブのみ','ハバンのみ','ナモのみ','バリブのみ','ロゼルのみ'
]
js_list='['+','.join('"'+x+'"' for x in allowed)+']'
replacement=f'''const CHAMPIONS_HELD_ITEMS={js_list};
const commonItems=CHAMPIONS_HELD_ITEMS;
const CHAMPIONS_HELD_ITEM_SET=new Set(CHAMPIONS_HELD_ITEMS);
function isChampionsHeldItem(v){{
 const x=String(v||'').trim();
 if(!x)return true;
 if(CHAMPIONS_HELD_ITEM_SET.has(x))return true;
 // Mega Stones are legal only for their corresponding Mega form; existing Mega logic locks those automatically.
 if(/ナイト[XY]?$/.test(x))return true;
 return false;
}}
function rejectUnavailableChampionsItem(v){{
 const x=String(v||'').trim();
 if(!x||isChampionsHeldItem(x))return false;
 alert(`「${{x}}」は現在のPokémon Championsで使用できる持ち物として登録されていません。`);
 return true;
}}
'''

s,n=re.subn(r'const commonItems=\[[^\n]*\];', replacement, s, count=1)
assert n==1, f'commonItems replacement count={n}'

old="items:(y.items||[]).map(x=>({name:x[0],pct:Number(x[1])||0})),"
new="items:(y.items||[]).map(x=>({name:x[0],pct:Number(x[1])||0})).filter(x=>isChampionsHeldItem(x.name)),"
assert old in s, 'rebuildEnvDb item line not found'
s=s.replace(old,new,1)

old="function clearBuild(){buildTeam=[];localStorage.removeItem('champ_build');renderBuildCurrent();renderBuildRoster();renderTeamCompletion();buildSuggestions.innerHTML='';buildSummary.textContent='2匹以上登録してください。'} function setItem(n,v){buildItems[n]=v;localStorage.setItem('champ_build_items',JSON.stringify(buildItems))}"
new="function clearBuild(){buildTeam=[];localStorage.removeItem('champ_build');renderBuildCurrent();renderBuildRoster();renderTeamCompletion();buildSuggestions.innerHTML='';buildSummary.textContent='2匹以上登録してください。'} function setItem(n,v){v=String(v||'').trim();if(rejectUnavailableChampionsItem(v)){buildItems[n]='';localStorage.setItem('champ_build_items',JSON.stringify(buildItems));renderBuildCurrent();return;}buildItems[n]=v;localStorage.setItem('champ_build_items',JSON.stringify(buildItems))}"
assert old in s, 'setItem block not found'
s=s.replace(old,new,1)

old="function updateSavedItem(i,v){\n if(!savedParty[i])return;\n const base=mons.find(m=>m.name===savedParty[i].name);\n savedParty[i].item=base?.mega?megaStoneFor(base):v;"
new="function updateSavedItem(i,v){\n if(!savedParty[i])return;\n const base=mons.find(m=>m.name===savedParty[i].name);\n if(!base?.mega && rejectUnavailableChampionsItem(v)){savedParty[i].item='';saveSavedParty();renderSavedEditors();renderSavedCompletion?.();return;}\n savedParty[i].item=base?.mega?megaStoneFor(base):String(v||'').trim();"
assert old in s, 'updateSavedItem block not found'
s=s.replace(old,new,1)

# Remove unavailable items from legacy Japanese display aliases so stale fallback data cannot present them as valid choices.
for bad in [
    'lifeorb:"いのちのたま",',
    'choiceband:"こだわりハチマキ",',
    'choicespecs:"こだわりメガネ",',
    'expertbelt:"たつじんのおび",',
    'weaknesspolicy:"じゃくてんほけん",',
    'lightclay:"ひかりのねんど",'
]:
    s=s.replace(bad,'')

# Clean already-saved invalid non-Mega held items when this version first opens.
marker='const yakkun={'
cleanup="""for(const k of Object.keys(buildItems)){if(buildItems[k]&&!isChampionsHeldItem(buildItems[k]))delete buildItems[k];}\nlocalStorage.setItem('champ_build_items',JSON.stringify(buildItems));\nsavedParty.forEach(x=>{if(x?.item&&!isChampionsHeldItem(x.item))x.item='';});\nlocalStorage.setItem('champ_saved_party',JSON.stringify(savedParty));\n"""
assert marker in s, 'yakkun marker not found'
s=s.replace(marker,cleanup+marker,1)

# Remove stale unavailable-item scoring bonuses. Choice Scarf remains valid and keeps its speed-control bonus.
s=s.replace("if([\"いのちのたま\",\"こだわりハチマキ\",\"こだわりメガネ\"].some(v=>item.includes(v)))clean+=2;", "")
s=s.replace("else if(['いのちのたま','たつじんのおび','こだわりハチマキ','こだわりメガネ'].some(x=>item.includes(x))){score+=2;itemReason='持ち物で火力を補強'}", "")

# Bump visible version label.
s=s.replace('Pokémon Champions Support — v18','Pokémon Champions Support — v18.1',2)

p.write_text(s,encoding='utf-8')
print('patched Champions held items:', len(allowed))
