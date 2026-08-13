from pathlib import Path
import subprocess,sys
subprocess.run([sys.executable,'scripts/v20_3_restore_home_classic.py'],check=True)
subprocess.run([sys.executable,'scripts/v20_3_auto_contrast.py'],check=True)
subprocess.run([sys.executable,'scripts/v20_4_sidebar_css.py'],check=True)
subprocess.run([sys.executable,'scripts/v20_4_sidebar_js.py'],check=True)
p=Path('index.html');s=p.read_text(encoding='utf-8')
marker='/* ===== v20.2 strict quick set logic ===== */'
if marker in s: raise SystemExit(0)
patch=r'''
<script>
/* ===== v20.2 strict quick set logic ===== */
(function(){
function exactSaved(m){return (savedParty||[]).find(x=>x?.name===m?.name)||null}
function strictMon(m){const q=exactSaved(m);if(!q)return {...m,set:{item:'',moves:[]}};const base=mons.find(x=>x.name===q.name)||m;return {...m,role:q.customRole||q.role||base.role||m.role,set:{item:base.mega?megaStoneFor(base):String(q.item||''),moves:(q.moves||[]).filter(x=>x?.name).map(x=>({...x}))}}}
function sync(){mine=mine.map(strictMon);try{localStorage.setItem('champ_mine',JSON.stringify(mine))}catch(e){}}
const old=quickAnalyze;
quickAnalyze=function(){sync();const out=old.apply(this,arguments);setTimeout(()=>{const r=document.getElementById('quickResult'),p=document.getElementById('quickPicks');if(!r||!p)return;let n=r.querySelector('.v202QuickSetNote');if(!n){n=document.createElement('div');n.className='v202QuickSetNote small';n.style.cssText='margin:0 0 10px;padding:8px 10px;border:1px solid var(--xline,#444);border-radius:10px;background:var(--xcard2,#222)';p.insertAdjacentElement('beforebegin',n)}n.textContent='自分側の持ち物・先制技・技範囲は「パーティ登録に保存した現在の型」だけで判定します。未登録の型は推測しません。';},0);return out};
if(typeof metaCandidateScoreV9==='function'){const om=metaCandidateScoreV9;metaCandidateScoreV9=function(m){const x=om(m);try{const p=v12Profile(m);x.reasons=(x.reasons||[]).filter(r=>!/スカーフ/.test(r)||p.scarf>=20).filter(r=>!/先制技/.test(r)||p.priority>=20).map(r=>/スカーフ/.test(r)?`環境スカーフ採用 ${Math.round(p.scarf)}%`:/先制技/.test(r)?`環境先制技採用 ${Math.round(p.priority)}%`:r)}catch(e){}return x}}
window.__V202_QUICK_TEST__={strict:strictMon({name:'__none__'}).set.item==='',priority:[{name:'かげうち'}].some(x=>['かげうち'].includes(x.name))};
})();
</script>
'''
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
