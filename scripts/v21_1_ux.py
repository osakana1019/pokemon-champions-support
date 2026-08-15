from pathlib import Path
import re

p = Path("index.html")
s = p.read_text(encoding="utf-8")
marker = "/* ===== v21.1 reliable navigation + usability ===== */"
if marker in s:
    raise SystemExit(0)

s = s.replace("Pokémon Champions Support — v21.0", "Pokémon Champions Support — v21.1")
s = s.replace('<div class="badge">v21.0</div>', '<div class="badge">v21.1</div>', 1)

patch = r'''<style id="v211-ux">
/* ===== v21.1 reliable navigation + usability ===== */
#v204Sidebar,#v205Rail,#v209Nav{display:none!important}
body.v204HasSidebar,body.v205RailOn,body.v209NavOn{padding-left:0!important}
body.v209NavOn .wrap,body.v205RailOn .wrap,body.v204HasSidebar .wrap{padding-left:24px!important}
#v211Nav{
 position:fixed;left:12px;top:12px;bottom:12px;z-index:1200;width:96px;
 display:flex;flex-direction:column;gap:7px;padding:10px 8px;
 border:1px solid var(--xline,#2a3548);border-radius:20px;
 background:color-mix(in srgb,var(--xcard,#111722) 96%,transparent);
 box-shadow:0 16px 42px #0005;backdrop-filter:blur(16px)
}
.v211Brand{
 min-height:44px;display:grid;place-items:center;border-radius:13px;
 background:var(--xaccent,#6da7ff);color:var(--xaccenttext,#07111f);
 font-size:13px;font-weight:950;letter-spacing:.08em
}
.v211NavSep{height:1px;background:var(--xline,#2a3548);margin:0 5px 3px}
#v211Nav button{
 position:relative;width:100%;min-height:62px;padding:7px 4px;border:0;border-radius:14px;
 display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;
 background:transparent;color:var(--xmuted,#9aa7ba);box-shadow:none
}
#v211Nav button:hover{background:var(--xsoft,#182437);color:var(--xtext,#f7f8fb);transform:none}
#v211Nav button.active{background:var(--xaccent,#6da7ff);color:var(--xaccenttext,#07111f)}
.v211Icon{font-size:20px;line-height:1}
.v211Label{font-size:10px;font-weight:900;line-height:1.05;white-space:nowrap}
.v211Count{
 position:absolute;right:5px;top:4px;min-width:18px;height:18px;padding:0 4px;border-radius:999px;
 display:grid;place-items:center;font-size:9px;font-weight:950;background:var(--xtext,#f7f8fb);
 color:var(--xbg,#080b11);border:2px solid var(--xcard,#111722)
}
.v211Bottom{margin-top:auto;display:grid;gap:7px}
body.v211NavOn .wrap{width:auto!important;max-width:1840px!important;margin:0 auto!important;padding:16px 24px 42px 128px!important}
button,input,select,textarea{font:inherit}
button{transition:background .14s ease,color .14s ease,border-color .14s ease,filter .14s ease}
button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{
 outline:3px solid color-mix(in srgb,var(--xaccent,#6da7ff) 68%,white);
 outline-offset:2px
}
.page.activePage{animation:v211PageIn .14s ease-out}
@keyframes v211PageIn{from{opacity:.45;transform:translateY(3px)}to{opacity:1;transform:none}}
.card{scroll-margin-top:14px}
#envPage .rankRow{min-height:64px}
#envPage .rankRow:hover{background:color-mix(in srgb,var(--xaccent,#6da7ff) 8%,#0e1521)}
#envPage .rankRow:focus-visible{outline:2px solid var(--xaccent,#6da7ff);outline-offset:1px}
#envPage .envGrid{align-items:start}
#quickPage button,#partyPage button,#envPage button{min-height:38px}
.v211RouteToast{
 position:fixed;left:50%;bottom:26px;z-index:1300;transform:translate(-50%,12px);
 padding:9px 13px;border-radius:999px;background:#0c1421e8;color:#eef4ff;border:1px solid #31415a;
 font-size:12px;font-weight:850;opacity:0;pointer-events:none;transition:.18s ease
}
.v211RouteToast.show{opacity:1;transform:translate(-50%,0)}
@media(max-width:1079px){
 #v211Nav{
  left:10px;right:10px;top:auto;bottom:10px;width:auto;height:70px;padding:7px;
  flex-direction:row;align-items:stretch;border-radius:18px;padding-bottom:max(7px,env(safe-area-inset-bottom))
 }
 .v211Brand,.v211NavSep{display:none}
 #v211Nav button{min-height:54px;flex:1;padding:5px 2px;border-radius:12px}
 .v211Icon{font-size:19px}.v211Label{font-size:9px}
 .v211Bottom{margin:0;display:flex;flex:1}
 .v211Bottom button{width:100%}
 body.v211NavOn .wrap,body.v209NavOn .wrap,body.v205RailOn .wrap,body.v204HasSidebar .wrap{
  width:auto!important;max-width:none!important;margin:0!important;padding:12px 12px 96px!important
 }
 .v211RouteToast{bottom:92px}
 #envPage .envGrid{grid-template-columns:1fr!important}
 #envPage .envGrid>section.card:first-child{position:static!important;max-height:none!important;overflow:visible!important}
 #envPage #envRankList{max-height:58vh!important;overflow:auto!important}
}
@media(max-width:560px){
 #v211Nav{left:6px;right:6px;bottom:6px;height:66px}
 .v211Label{font-size:8px}.v211Icon{font-size:18px}
 .wrap header{align-items:flex-start}
 .wrap header .badge{padding:5px 7px;font-size:9px}
 .card{padding:12px;border-radius:15px}
 .homeActions,.toolbar,.v205PartyActions,.v205AnalysisBtns{gap:7px}
 .homeActions button,.toolbar button,.v205PartyActions button,.v205AnalysisBtns button{flex:1;min-width:120px}
}
</style>
<script>
(function(){
'use strict';
const LABELS={home:'ホーム',quick:'選出',party:'パーティ',env:'環境'};
let routing=false,toastTimer=0;

function ensureNav(){
 let n=document.getElementById('v211Nav');
 if(n)return n;
 n=document.createElement('nav');
 n.id='v211Nav';
 n.setAttribute('aria-label','メインナビゲーション');
 n.innerHTML=`
  <div class="v211Brand">CS</div><div class="v211NavSep"></div>
  <button type="button" data-v211-page="home" aria-label="ホーム"><span class="v211Icon">⌂</span><span class="v211Label">ホーム</span></button>
  <button type="button" data-v211-page="quick" aria-label="クイック選出"><span class="v211Icon">⚡</span><span class="v211Label">選出</span></button>
  <button type="button" data-v211-page="party" aria-label="パーティ"><span class="v211Icon">6</span><span class="v211Label">パーティ</span><span class="v211Count" data-v211-count>0</span></button>
  <button type="button" data-v211-page="env" aria-label="環境データ"><span class="v211Icon">▥</span><span class="v211Label">環境</span></button>
  <div class="v211Bottom"><button type="button" data-v211-settings aria-label="表示設定"><span class="v211Icon">⚙</span><span class="v211Label">設定</span></button></div>`;
 document.body.appendChild(n);
 document.body.classList.add('v211NavOn');
 n.querySelectorAll('[data-v211-page]').forEach(b=>b.addEventListener('click',()=>route(b.dataset.v211Page)));
 n.querySelector('[data-v211-settings]')?.addEventListener('click',openSettingsSafe);
 return n;
}

function openSettingsSafe(){
 const panel=document.getElementById('v202SettingsPanel');
 if(panel){panel.classList.add('show');return}
 document.getElementById('v202SettingsBtn')?.click();
}

function normalize(name){
 if(name==='saved')return {page:'party',tab:'edit'};
 if(name==='build')return {page:'party',tab:'analysis'};
 if(name==='party')return {page:'party',tab:null};
 if(['home','quick','env'].includes(name))return {page:name,tab:null};
 return {page:'home',tab:null};
}

function renderFor(page){
 try{
  if(page==='home'&&typeof renderHomeV18==='function')renderHomeV18();
  if(page==='quick'){
   if(typeof renderSelected==='function')renderSelected();
   if(typeof renderRoster==='function')renderRoster();
   if(typeof renderOppQuickGrid==='function')renderOppQuickGrid();
  }
  if(page==='env'){
   if(typeof renderEnvList==='function')renderEnvList();
   else if(typeof renderEnvironment==='function')renderEnvironment();
   else if(typeof renderEnvRanking==='function')renderEnvRanking();
  }
 }catch(e){console.warn('v21.1 render',page,e)}
}

function directPage(page){
 const target=document.getElementById(page+'Page');
 if(!target)return false;
 document.querySelectorAll('.page').forEach(x=>{
  x.classList.remove('activePage');
  if(x.id!=='savedPage'&&x.id!=='buildPage')x.style.removeProperty('display');
 });
 target.style.removeProperty('display');
 target.classList.add('activePage');
 document.querySelectorAll('.appnav button').forEach(x=>x.classList.remove('activeApp'));
 const old=document.getElementById('app'+page.charAt(0).toUpperCase()+page.slice(1)+'Btn');
 old?.classList.add('activeApp');
 try{currentPage=page}catch(e){}
 renderFor(page);
 return true;
}

function showToast(page){
 let t=document.getElementById('v211RouteToast');
 if(!t){t=document.createElement('div');t.id='v211RouteToast';t.className='v211RouteToast';document.body.appendChild(t)}
 t.textContent=(LABELS[page]||page)+'を開きました';
 clearTimeout(toastTimer);
 requestAnimationFrame(()=>t.classList.add('show'));
 toastTimer=setTimeout(()=>t.classList.remove('show'),850);
}

function setHash(page,replace){
 const hash='#/'+page;
 if(location.hash===hash)return;
 try{history[replace?'replaceState':'pushState']({csPage:page},'',hash)}catch(e){}
}

function activePage(){
 const id=document.querySelector('.page.activePage')?.id||'';
 if(id==='partyPage')return 'party';
 if(id==='homePage')return 'home';
 if(id==='quickPage')return 'quick';
 if(id==='envPage')return 'env';
 if(id==='savedPage'||id==='buildPage')return 'party';
 return 'home';
}

function refreshNav(){
 const n=ensureNav(),p=activePage();
 n.querySelectorAll('[data-v211-page]').forEach(b=>{
  const on=b.dataset.v211Page===p;
  b.classList.toggle('active',on);
  if(on)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');
 });
 const c=n.querySelector('[data-v211-count]');
 if(c){try{c.textContent=String((savedParty||[]).length)}catch(e){c.textContent='0'}}
}

function route(name,opts){
 opts=opts||{};
 const r=normalize(name);
 if(routing)return;
 routing=true;
 try{
  if(r.page==='party'&&typeof window.v205OpenParty==='function'){
   window.v205OpenParty(r.tab||undefined);
  }else if(r.page==='party'){
   directPage(r.tab==='analysis'?'build':'saved');
  }else{
   directPage(r.page);
  }
  refreshNav();
  if(opts.history!==false)setHash(r.page,!!opts.replace);
  if(opts.scroll!==false)window.scrollTo({top:0,left:0,behavior:'instant'});
  if(opts.toast!==false)showToast(r.page);
 }finally{
  setTimeout(()=>{routing=false},0);
 }
}

window.switchPage=function(name){return route(name)};
window.v211Route=route;

function routeFromLocation(){
 const m=location.hash.match(/^#\/(home|quick|party|env)$/);
 if(m)route(m[1],{history:false,scroll:false,toast:false});
 else refreshNav();
}

ensureNav();
refreshNav();
setTimeout(()=>{ensureNav();refreshNav();routeFromLocation()},0);
setTimeout(refreshNav,120);
setInterval(refreshNav,1200);
window.addEventListener('popstate',routeFromLocation);
window.addEventListener('hashchange',routeFromLocation);
new MutationObserver(refreshNav).observe(document.body,{subtree:true,attributes:true,attributeFilter:['class']});
window.__V211_TEST__={route,activePage,nav:()=>!!document.getElementById('v211Nav'),env:()=>route('env',{toast:false})};
})();
</script>'''

if "</body>" not in s:
    raise SystemExit("body close not found")
s = s.replace("</body>", patch + "\n</body>", 1)
p.write_text(s, encoding="utf-8")
print("Applied v21.1 reliable navigation + usability")
