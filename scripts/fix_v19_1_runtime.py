from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='/* ===== v19.1b: elite summary runtime hardening ===== */'
if marker in s:
    raise SystemExit(0)

old="""function v191AppendEliteSummary(){
  const card=document.getElementById('v19BuildIntel');if(!card)return;
  card.querySelector('.v191EliteBox')?.remove();
  const rows=v191BestEliteTeamMatches();if(!rows.length||!buildTeam.length)return;
  const box=document.createElement('div');box.className='v191EliteBox';
  box.innerHTML=`<b>上位プレイヤー構築との一致</b><br>`+rows.map(x=>{
    const used=x.matched.map(m=>m.name).join('・');
    const next=x.missing.slice(0,3).join('・');
    return `・${x.build.season} ${x.build.achievement}：${v19Esc? v19Esc(used):used}${next?` → 同居実績 ${v19Esc? v19Esc(next):next}`:''}`;
  }).join('<br>');
  card.appendChild(box);
}

// v19RenderBuildIntel is scoped inside v19, so observe the card and append our elite summary after re-renders.
const v191BuildRoot=document.getElementById('buildPage')||document.body;
new MutationObserver(()=>setTimeout(v191AppendEliteSummary,0)).observe(v191BuildRoot,{childList:true,subtree:true});
setTimeout(v191AppendEliteSummary,0);
"""
new="""function v191AppendEliteSummary(){
  const card=document.getElementById('v19BuildIntel');if(!card)return;
  const rows=v191BestEliteTeamMatches();
  const esc=z=>String(z??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\\\"/g,'&quot;');
  const html=(!rows.length||!buildTeam.length)?'':`<b>上位プレイヤー構築との一致</b><br>`+rows.map(x=>{
    const used=x.matched.map(m=>m.name).join('・');
    const next=x.missing.slice(0,3).join('・');
    return `・${esc(x.build.season)} ${esc(x.build.achievement)}：${esc(used)}${next?` → 同居実績 ${esc(next)}`:''}`;
  }).join('<br>');
  let box=card.querySelector('.v191EliteBox');
  if(!html){if(box)box.remove();return;}
  if(!box){box=document.createElement('div');box.className='v191EliteBox';card.appendChild(box);}
  if(box.innerHTML!==html)box.innerHTML=html;
}

// Append after the existing v19 builder renderer; avoid a self-triggering MutationObserver loop.
const _v191RenderBuildCurrent=renderBuildCurrent;
renderBuildCurrent=function(){
  const r=_v191RenderBuildCurrent.apply(this,arguments);
  setTimeout(v191AppendEliteSummary,40);
  return r;
};
setTimeout(v191AppendEliteSummary,60);
/* ===== v19.1b: elite summary runtime hardening ===== */
"""
if old not in s:
    raise SystemExit('v19.1 runtime block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
