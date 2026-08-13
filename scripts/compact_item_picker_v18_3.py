from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

if 'id="v18-item-picker"' in s:
    print('compact item picker already applied')
    raise SystemExit(0)

# Visible version bump.
s=s.replace('Pokémon Champions Support — v18.2','Pokémon Champions Support — v18.3',2)

css=r'''
<style id="v18-item-picker">
.itemSuggestWrap{position:relative;width:100%}
.itemSuggestWrap .buildItemInput,.itemSuggestWrap .savedItem{width:100%}
.itemSuggestBox{
 position:absolute;left:0;right:0;top:calc(100% + 4px);z-index:95;
 display:none;max-height:218px;overflow:auto;
 background:#0b111b;border:1px solid #3b4d68;border-radius:10px;
 box-shadow:0 12px 30px rgba(0,0,0,.42);padding:4px;
}
.itemSuggestBox.show{display:block}
.itemSuggestItem{
 min-height:32px;display:flex;align-items:center;justify-content:space-between;gap:8px;
 padding:6px 8px;border-radius:7px;cursor:pointer;font-size:11px;color:#eef4ff;
}
.itemSuggestItem:hover,.itemSuggestItem.active{background:#17243a}
.itemSuggestMeta{font-size:8px;font-weight:900;white-space:nowrap;color:#a9c8ff;
 border:1px solid #304c70;background:#11223a;border-radius:999px;padding:2px 5px}
.itemSuggestMeta.metaTop{color:#ffe09b;border-color:#69572e;background:#2a2313}
.itemSuggestHint{font-size:9px;color:#7f91aa;margin-top:3px;text-align:left}
</style>
'''
assert '</head>' in s
s=s.replace('</head>',css+'</head>',1)

js=r'''
// v18.3 compact held-item picker: Pokemon-specific usage first, then broadly popular items.
const POPULAR_HELD_ITEMS=[
 'きあいのタスキ','こだわりスカーフ','いのちのたま','オボンのみ','たべのこし','ラムのみ',
 'たつじんのおび','ひかりのねんど','メンタルハーブ','こうかくレンズ','ちからのハチマキ','ものしりメガネ'
];
function normalizeHeldItemSearch(v){
 return String(v||'').toLowerCase().normalize('NFKC').replace(/[・･\sー\-]/g,'');
}
function pokemonHeldItemUsageOrder(monName){
 const rows=yakkun?.[monName]?.items||[];
 const out=[];
 for(const row of rows){
  const raw=Array.isArray(row)?row[0]:(row?.name||'');
  const ja=(typeof displayEnvTerm==='function'?displayEnvTerm('items',raw):raw)||raw;
  if(!ja||!isChampionsHeldItem(ja)||/ナイト[XY]?$/.test(ja)||out.includes(ja))continue;
  out.push(ja);
 }
 return out;
}
function heldItemSuggestions(monName,query=''){
 const top=pokemonHeldItemUsageOrder(monName);
 const ordered=[];
 for(const x of [...top,...POPULAR_HELD_ITEMS,...CHAMPIONS_HELD_ITEMS]){
  if(isChampionsHeldItem(x)&&!ordered.includes(x))ordered.push(x);
 }
 const q=normalizeHeldItemSearch(query);
 const filtered=q?ordered.filter(x=>normalizeHeldItemSearch(x).includes(q)):ordered;
 return filtered.slice(0,8).map(name=>({
  name,
  meta:top.includes(name)?'採用上位':POPULAR_HELD_ITEMS.includes(name)?'人気':'',
  top:top.includes(name)
 }));
}
function showHeldItemSuggestions(input){
 const wrap=input.closest('.itemSuggestWrap'),box=wrap?.querySelector('.itemSuggestBox');
 if(!box||input.readOnly)return;
 const list=heldItemSuggestions(input.dataset.mon||'',input.value);
 box.innerHTML=list.map(x=>`<div class="itemSuggestItem" onpointerdown="event.preventDefault();chooseHeldItemSuggestion(this.closest('.itemSuggestWrap').querySelector('input'),'${x.name.replace(/'/g,"\\'")}')"><span>${x.name}</span>${x.meta?`<span class="itemSuggestMeta ${x.top?'metaTop':''}">${x.meta}</span>`:''}</div>`).join('');
 box.classList.toggle('show',list.length>0);
}
function hideHeldItemSuggestions(input){
 setTimeout(()=>input.closest('.itemSuggestWrap')?.querySelector('.itemSuggestBox')?.classList.remove('show'),120);
}
function chooseHeldItemSuggestion(input,name){
 input.value=name;
 if(input.dataset.itemScope==='saved')updateSavedItem(Number(input.dataset.itemKey),name);
 else if(input.dataset.itemScope==='build')setItem(input.dataset.itemKey,name);
 input.closest('.itemSuggestWrap')?.querySelector('.itemSuggestBox')?.classList.remove('show');
}
'''
marker="for(const k of Object.keys(buildItems)){if(buildItems[k]&&!isChampionsHeldItem(buildItems[k]))delete buildItems[k];}"
assert marker in s
s=s.replace(marker,js+'\n'+marker,1)

# Replace saved held-item input with compact custom picker.
pat=r'''function savedItemInputHtml\(m,i\)\{.*?\n\}\n\nfunction renderSavedEditors'''
repl=r'''function savedItemInputHtml(m,i){
 const forced=m.mega?megaStoneFor(m):"";
 if(m.mega && savedParty[i]){
  if(savedParty[i].item!==forced){savedParty[i].item=forced;saveSavedParty();}
  return `<input class="savedItem" value="${forced.replace(/"/g,"&quot;")}" readonly title="メガシンカには対応メガナイトが必要です">`;
 }
 return `<div class="itemSuggestWrap">
  <input class="savedItem" value="${(m.item||"").replace(/"/g,"&quot;")}" placeholder="持ち物を検索"
   autocomplete="off" data-item-scope="saved" data-item-key="${i}" data-mon="${m.name.replace(/"/g,'&quot;')}"
   onfocus="showHeldItemSuggestions(this)"
   oninput="showHeldItemSuggestions(this)"
   onblur="hideHeldItemSuggestions(this)"
   onchange="updateSavedItem(${i},this.value)">
  <div class="itemSuggestBox"></div>
 </div>`;
}

function renderSavedEditors'''
s,n=re.subn(pat,repl,s,count=1,flags=re.S)
assert n==1, f'saved item input replacement count={n}'

# Remove the old giant native datalist from saved-party rendering.
s=s.replace(" }).join('')+`<datalist id=\"savedItems\">${commonItems.map(x=>`<option value=\"${x}\">`).join('')}</datalist>`;"," }).join('');",1)

# Replace helper used for build held-item inputs.
pat=r'''function buildItemInputHtml\(m,item\)\{.*?\n\}\n\nfunction renderBuildCurrent'''
repl=r'''function buildItemInputHtml(m,item){
 const safe=String(item||"").replace(/"/g,"&quot;");
 if(m?.mega)return `<input class="buildItemInput" value="${safe}" readonly aria-readonly="true">`;
 return `<div class="itemSuggestWrap">
  <input class="buildItemInput" value="${safe}" placeholder="持ち物を検索" autocomplete="off"
   data-item-scope="build" data-item-key="${m.name.replace(/"/g,'&quot;')}" data-mon="${m.name.replace(/"/g,'&quot;')}"
   onclick="event.stopPropagation()" onpointerdown="event.stopPropagation()"
   onfocus="showHeldItemSuggestions(this)" oninput="showHeldItemSuggestions(this)" onblur="hideHeldItemSuggestions(this)"
   onchange="setItem('${m.name.replace(/'/g,"\\'")}',this.value)">
  <div class="itemSuggestBox"></div>
 </div>`;
}

function renderBuildCurrent'''
s,n=re.subn(pat,repl,s,count=1,flags=re.S)
assert n==1, f'build helper replacement count={n}'

# Replace the inline build input with the helper, and remove its native datalist.
old=r'''   <input class="buildItemInput" list="items" value="${item.replace(/"/g,'&quot;')}" placeholder="持ち物"
    onclick="event.stopPropagation()" onpointerdown="event.stopPropagation()"
    onchange="setItem('${m.name.replace(/'/g,"\'")}',this.value)">
  </div>`;
 }).join('')+`<datalist id="items">${commonItems.map(x=>`<option value="${x}">`).join('')}</datalist>`;'''
new=r'''   ${buildItemInputHtml(m,item)}
  </div>`;
 }).join('');'''
assert old in s, 'inline build held-item block not found'
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('applied compact held-item picker v18.3')
