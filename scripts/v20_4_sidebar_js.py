from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8')
marker='/* ===== v20.9 rebuilt nav final ===== */'
if marker in s: raise SystemExit(0)
if 'V208_ZUKAN_ART' not in s or 'zukan.pokemon.co.jp' not in s:
    raise SystemExit('official zukan artwork map missing')
js=r'''<script>
/* ===== v20.9 rebuilt nav final ===== */
(function(){
'use strict';
function openSettings(){const p=document.getElementById('v202SettingsPanel');if(p)p.classList.add('show');else document.getElementById('v202SettingsBtn')?.click()}
function make(){
 document.getElementById('v205Rail')?.remove();
 document.getElementById('v209Nav')?.remove();
 const n=document.createElement('aside');n.id='v209Nav';n.setAttribute('aria-label','メインメニュー');
 n.innerHTML=`<div class="v209Brand">CS</div><div class="v209Sep"></div>
 <button data-k="home"><span class="v209Ico">⌂</span><span class="v209Lbl">ホーム</span></button>
 <button data-k="quick"><span class="v209Ico">⚡</span><span class="v209Lbl">選出</span></button>
 <button data-k="party"><span class="v209Ico">6</span><span class="v209Lbl">パーティ</span><span class="v209Count">0</span></button>
 <button data-k="env"><span class="v209Ico">▥</span><span class="v209Lbl">環境</span></button>
 <div class="v209Bottom"><button data-k="settings"><span class="v209Ico">⚙</span><span class="v209Lbl">設定</span></button></div>`;
 document.body.appendChild(n);document.body.classList.add('v209NavOn');
 n.querySelector('[data-k=home]').onclick=()=>switchPage('home');
 n.querySelector('[data-k=quick]').onclick=()=>switchPage('quick');
 n.querySelector('[data-k=party]').onclick=()=>typeof v205OpenParty==='function'?v205OpenParty():switchPage('saved');
 n.querySelector('[data-k=env]').onclick=()=>switchPage('env');
 n.querySelector('[data-k=settings]').onclick=openSettings;
}
function active(){
 const n=document.getElementById('v209Nav');if(!n)return;
 const id=document.querySelector('.page.activePage')?.id||'';
 const k=id==='homePage'?'home':id==='quickPage'?'quick':id==='partyPage'?'party':id==='envPage'?'env':'';
 n.querySelectorAll('button[data-k]').forEach(b=>b.classList.toggle('active',b.dataset.k===k));
 const c=n.querySelector('.v209Count');if(c){try{c.textContent=String((savedParty||[]).length)}catch(e){c.textContent='0'}}
}
make();active();setTimeout(active,50);setInterval(active,500);
window.__V209_TEST__={nav:()=>document.querySelectorAll('#v209Nav .v209Lbl').length,zukan:()=>Object.keys(V208_ZUKAN_ART||{}).length,source:'zukan.pokemon.co.jp'};
})();
</script>'''
s=s.replace('</body>',js+'\n</body>',1)
p.write_text(s,encoding='utf-8')
