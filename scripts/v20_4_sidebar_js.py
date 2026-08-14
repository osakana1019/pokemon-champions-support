from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8')
marker='/* ===== v20.6 source clarity + meter normalization ===== */'
if marker in s: raise SystemExit(0)
js=r'''<script>
/* ===== v20.6 source clarity + meter normalization ===== */
(function(){
'use strict';
const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
function sourceTeam(){try{return (savedParty||[]).slice(0,6)}catch(e){return []}}
function sourceSig(){return sourceTeam().map(m=>`${m?.name||''}|${m?.item||''}|${(m?.moves||[]).map(x=>x?.name||'').join(',')}`).join('||')}
let last='';
function renderSource(force=false){
 const result=document.getElementById('buildResult'),summary=document.getElementById('buildSummary');if(!result||!summary)return;
 const sig=sourceSig();if(!force&&sig===last&&document.getElementById('v206PartySource'))return;last=sig;
 let box=document.getElementById('v206PartySource');if(!box){box=document.createElement('div');box.id='v206PartySource';summary.parentNode.insertBefore(box,summary)}
 const team=sourceTeam();
 const cells=Array.from({length:6},(_,i)=>{const m=team[i];if(!m)return '<div class="v206SourceEmpty">空き</div>';let src='';try{src=sprite(m)}catch(e){};let fb='';try{fb=fallback(m)}catch(e){};return `<div class="v206SourceMon" title="${esc(m.name)}"><img src="${esc(src)}" ${fb?`onerror="this.onerror=null;this.src='${String(fb).replace(/'/g,"\\'")}'"`:''}><span>${esc(m.name)}</span></div>`}).join('');
 box.innerHTML=`<div class="v206SourceHead"><b>このパーティを基準に総合候補を計算</b><span>${team.length}/6体 ・ 技/持ち物も反映</span></div><div class="v206SourceMons">${cells}</div>`;
 let legend=document.getElementById('v206MeterLegend');if(!legend){legend=document.createElement('div');legend.id='v206MeterLegend';legend.className='v206MeterNote';const suggestions=document.getElementById('buildSuggestions');suggestions?.parentNode.insertBefore(legend,suggestions)}if(legend)legend.textContent='総合適合度は0〜100。表示％とバーの長さを同じ値に統一しています。';
}
function meterPct(card){const t=card.querySelector('.compatPct')?.textContent||'';const m=t.match(/(-?\d+(?:\.\d+)?)\s*%/);return m?Math.max(0,Math.min(100,Number(m[1]))):null}
function normalizeMeters(){
 document.querySelectorAll('#buildSuggestions .v12BuildPick').forEach(card=>{const p=meterPct(card),bar=card.querySelector('.compatBar>div');if(p===null||!bar)return;bar.style.setProperty('width',p+'%','important');bar.dataset.fit=String(p);const pct=card.querySelector('.compatPct');if(pct){const raw=pct.textContent.match(/(-?\d+(?:\.\d+)?)\s*%/);if(raw)pct.textContent=raw[1]+'%'}});
 renderSource();
}
function install(){renderSource(true);normalizeMeters();const target=document.getElementById('buildSuggestions');if(target&&!target.dataset.v206watch){target.dataset.v206watch='1';new MutationObserver(()=>{renderSource();normalizeMeters()}).observe(target,{childList:true,subtree:true,characterData:true})}}
const oldAnalyze=window.v205AnalyzeParty;if(typeof oldAnalyze==='function'){window.v205AnalyzeParty=function(){renderSource(true);const r=oldAnalyze.apply(this,arguments);setTimeout(()=>{renderSource(true);normalizeMeters()},50);return r}}
const oldOpen=window.v205OpenParty;if(typeof oldOpen==='function'){window.v205OpenParty=function(){const r=oldOpen.apply(this,arguments);setTimeout(()=>{renderSource(true);normalizeMeters()},0);return r}}
install();setInterval(()=>{if(sourceSig()!==last)renderSource(true);normalizeMeters()},1200);window.__V206_TEST__={source:!!document.getElementById('v206PartySource'),meters:typeof normalizeMeters==='function'};
})();
</script>'''
s=s.replace('</body>',js+'\n</body>',1);p.write_text(s,encoding='utf-8')
