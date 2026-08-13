from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

s = s.replace('Pokémon Champions Support — v18.5', 'Pokémon Champions Support — v18.6')

old = '''renderCounterDatalist=function(){
 const dl=document.getElementById('counterPokemonOptions');if(!dl)return;
 dl.innerHTML=sortBrowseMons(mons,'usage').map(m=>{
  const canonical=v184EscAttr(m.name),hira=v184EscAttr(kataToHira(m.name));
  return `<option value="${canonical}"></option>${hira!==canonical?`<option value="${hira}" label="${canonical}"></option>`:''}`;
 }).join('');
};'''
new = '''renderCounterDatalist=function(){
 const dl=document.getElementById('counterPokemonOptions');if(!dl)return;
 // Fallback datalist keeps one visible entry per Pokemon. Hiragana matching is handled by the custom picker below.
 dl.innerHTML=sortBrowseMons(mons,'usage').map(m=>`<option value="${v184EscAttr(m.name)}"></option>`).join('');
};'''
if old not in s:
    raise SystemExit('counter datalist block not found')
s = s.replace(old, new, 1)

marker = '\n</script></body></html>'
if marker not in s:
    raise SystemExit('closing marker not found')

addon = r'''

/* ===== v18.6: single-name counter picker ===== */
function v186CounterCandidates(value){
 const q=v184NormalizeSearch(value);
 const seen=new Set(),out=[];
 for(const m of sortBrowseMons(mons,'usage')){
  if(seen.has(m.name))continue;
  seen.add(m.name);
  if(q&&!v184NormalizeSearch(m.name).includes(q))continue;
  out.push(m);
  if(out.length>=9)break;
 }
 return out;
}
function initCounterPickerV186(){
 const input=document.getElementById('counterPokemonInput');
 if(!input||input.dataset.v186Picker==='1')return;
 input.dataset.v186Picker='1';
 input.removeAttribute('list');

 const parent=input.parentNode;
 const wrap=document.createElement('div');
 wrap.className='counterSuggestWrapV186';
 parent.insertBefore(wrap,input);
 wrap.appendChild(input);
 const box=document.createElement('div');
 box.className='counterSuggestBoxV186';
 wrap.appendChild(box);

 if(!document.getElementById('counter-picker-v186-style')){
  const style=document.createElement('style');
  style.id='counter-picker-v186-style';
  style.textContent=`
   .counterSuggestWrapV186{position:relative;flex:1 1 260px;min-width:0}
   .counterSuggestWrapV186 #counterPokemonInput{width:100%}
   .counterSuggestBoxV186{position:absolute;left:0;right:0;top:calc(100% + 5px);z-index:120;display:none;max-height:270px;overflow:auto;padding:5px;background:#0b111b;border:1px solid #3b4d68;border-radius:11px;box-shadow:0 14px 32px rgba(0,0,0,.46)}
   .counterSuggestBoxV186.show{display:block}
   .counterSuggestRowV186{width:100%;min-height:34px;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:7px 9px;border:0;border-radius:8px;background:transparent;color:#eef4ff;text-align:left;font-size:12px}
   .counterSuggestRowV186:hover,.counterSuggestRowV186.active{background:#17243a}
   .counterSuggestRankV186{font-size:9px;color:#8ea2bd;font-weight:850;white-space:nowrap}
  `;
  document.head.appendChild(style);
 }

 let active=-1;
 const rows=()=>Array.from(box.querySelectorAll('.counterSuggestRowV186'));
 function setActive(i){
  const rs=rows();
  if(!rs.length){active=-1;return;}
  active=Math.max(0,Math.min(rs.length-1,i));
  rs.forEach((r,j)=>r.classList.toggle('active',j===active));
  rs[active]?.scrollIntoView({block:'nearest'});
 }
 function choose(name){
  input.value=name;
  box.classList.remove('show');
  active=-1;
  input.focus();
 }
 function render(){
  const list=v186CounterCandidates(input.value);
  box.innerHTML='';
  active=-1;
  if(!list.length){box.classList.remove('show');return;}
  for(const m of list){
   const b=document.createElement('button');
   b.type='button';b.className='counterSuggestRowV186';b.dataset.name=m.name;
   const name=document.createElement('span');name.textContent=m.name;
   const rank=document.createElement('span');rank.className='counterSuggestRankV186';rank.textContent=m.usageRank&&m.usageRank<=150?`環境 #${m.usageRank}`:'';
   b.append(name,rank);
   b.addEventListener('mousedown',e=>{e.preventDefault();choose(m.name);});
   box.appendChild(b);
  }
  box.classList.add('show');
 }
 input.addEventListener('focus',render);
 input.addEventListener('input',render);
 input.addEventListener('keydown',e=>{
  const rs=rows();
  if(e.key==='ArrowDown'&&rs.length){e.preventDefault();setActive(active<0?0:active+1);}
  else if(e.key==='ArrowUp'&&rs.length){e.preventDefault();setActive(active<0?rs.length-1:active-1);}
  else if(e.key==='Enter'&&active>=0&&rs[active]){e.preventDefault();choose(rs[active].dataset.name);}
  else if(e.key==='Escape'){box.classList.remove('show');active=-1;}
 });
 input.addEventListener('blur',()=>setTimeout(()=>{box.classList.remove('show');active=-1;},120));
}
initCounterPickerV186();
'''

s = s.replace(marker, addon + marker, 1)
p.write_text(s, encoding='utf-8')
print('patched index.html to v18.6')
