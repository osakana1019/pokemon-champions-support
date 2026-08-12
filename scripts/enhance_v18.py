from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'data-app-version="v18-useful"' in s:
    print('v18 already applied')
    raise SystemExit(0)

s = s.replace('<title>Pokémon Champions Support — WEB v17</title>', '<title>Pokémon Champions Support — v18</title>')
s = s.replace('<meta property="og:title" content="Pokémon Champions Support — WEB v17">', '<meta property="og:title" content="Pokémon Champions Support — v18">')
s = s.replace('<body data-app-version="v17-web">', '<body data-app-version="v18-useful">')
s = s.replace('<div class="badge">WEB v17</div>', '<div class="badge">v18 USEFUL</div>')
s = s.replace('<div class="sub">選出・構築・環境データ</div>', '<div class="sub">構築 → 対策 → 選出を1つにつなぐ実戦サポート</div>')

nav_old = '<nav class="appnav"><button id="appQuickBtn" class="activeApp" onclick="switchPage(\'quick\')">⚡ クイック選出</button><button id="appSavedBtn" onclick="switchPage(\'saved\')">💾 パーティ登録</button><button id="appBuildBtn" onclick="switchPage(\'build\')">🧩 パーティ構築</button><button id="appEnvBtn" onclick="switchPage(\'env\')">📊 環境データ</button></nav>'
nav_new = '<nav class="appnav"><button id="appHomeBtn" class="activeApp" onclick="switchPage(\'home\')">⌂ ホーム</button><button id="appQuickBtn" onclick="switchPage(\'quick\')">⚡ クイック選出</button><button id="appSavedBtn" onclick="switchPage(\'saved\')">💾 パーティ登録</button><button id="appBuildBtn" onclick="switchPage(\'build\')">🧩 パーティ構築</button><button id="appEnvBtn" onclick="switchPage(\'env\')">📊 環境データ</button></nav>'
if nav_old not in s:
    raise SystemExit('nav target not found')
s = s.replace(nav_old, nav_new, 1)

home_html = r'''
<div id="homePage" class="page activePage">
  <section class="card homeHeroV18">
    <div class="homeHeroCopy">
      <div class="homeEyebrow">MATCH DAY DASHBOARD</div>
      <h2>次にやることが、すぐ分かる。</h2>
      <div id="homeNextText" class="homeLead">保存状況を見ておすすめの次の操作を表示します。</div>
      <div class="homeActions">
        <button id="homePrimaryAction" class="primary" onclick="homePrimaryAction()">おすすめの操作</button>
        <button onclick="homeUseSavedQuick()">登録パーティで選出</button>
        <button onclick="switchPage('build')">構築をチェック</button>
      </div>
    </div>
    <div class="homeScorePanel">
      <div class="small">YOUR SETUP</div>
      <div id="homeSetupScore" class="homeSetupScore">0%</div>
      <div id="homeSetupLabel" class="small">準備状況</div>
      <div class="compatBar"><div id="homeSetupBar" style="width:0%"></div></div>
    </div>
  </section>

  <section class="homeGridV18">
    <div class="card homePanelV18">
      <div class="homePanelHead"><div><div class="homeEyebrow">MY TEAM</div><h2>登録パーティ</h2></div><button onclick="switchPage('saved')">編集</button></div>
      <div id="homePartyPreview" class="homePartyPreview"></div>
      <div id="homePartyHint" class="small"></div>
    </div>

    <div class="card homePanelV18">
      <div class="homePanelHead"><div><div class="homeEyebrow">QUICK TOOLS</div><h2>すぐ使う</h2></div></div>
      <div class="homeToolGrid">
        <button class="homeTool" onclick="homeUseSavedQuick()"><b>⚡ 選出する</b><span>登録6体を読み込んで相手を選ぶ</span></button>
        <button class="homeTool" onclick="switchPage('build')"><b>🧩 構築を改善</b><span>弱点・役割・おすすめ候補を確認</span></button>
        <button class="homeTool" onclick="homeFocusCounter()"><b>🎯 苦手対策</b><span>苦手な1体から回答候補を探す</span></button>
        <button class="homeTool" onclick="switchPage('env')"><b>📊 環境を見る</b><span>上位ポケモンの採用データを確認</span></button>
      </div>
    </div>
  </section>

  <section class="card homePanelV18">
    <div class="homePanelHead"><div><div class="homeEyebrow">META SNAPSHOT</div><h2>環境上位</h2></div><button onclick="switchPage('env')">すべて見る</button></div>
    <div id="homeMetaTop" class="homeMetaTop"></div>
  </section>
</div>
'''
quick_marker = '<div id="quickPage" class="page activePage">'
if quick_marker not in s:
    raise SystemExit('quick page marker not found')
s = s.replace(quick_marker, home_html + '\n<div id="quickPage" class="page">', 1)

css = r'''
/* ===== v18 useful dashboard ===== */
.appnav{grid-template-columns:repeat(5,minmax(0,1fr))}
.homeHeroV18{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(220px,.5fr);gap:18px;align-items:stretch;padding:24px;background:radial-gradient(circle at 90% 10%,rgba(109,167,255,.14),transparent 34%),linear-gradient(145deg,#111a29,#0d131e 62%)}
.homeHeroCopy{display:flex;flex-direction:column;justify-content:center;min-height:190px}.homeHeroCopy h2{font-size:clamp(24px,3vw,38px);margin:5px 0 8px}.homeEyebrow{font-size:10px;letter-spacing:.16em;font-weight:900;color:#8fb8ff}.homeLead{color:#c5d0df;line-height:1.7;max-width:760px}.homeActions{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}.homeActions button{min-height:42px}
.homeScorePanel{border:1px solid #2d3d55;border-radius:18px;background:#0b111b;padding:18px;display:flex;flex-direction:column;justify-content:center}.homeSetupScore{font-size:52px;font-weight:950;letter-spacing:-.04em;color:#b8d2ff;margin:4px 0}.homeGridV18{display:grid;grid-template-columns:1.05fr .95fr;gap:16px}.homePanelV18{margin-bottom:16px}.homePanelHead{display:flex;align-items:center;justify-content:space-between;gap:12px}.homePanelHead h2{margin:3px 0 0}.homePartyPreview{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px;margin:14px 0 8px}.homePartyMon,.homePartyEmpty{min-width:0;border:1px solid #2c3a4f;border-radius:14px;background:#0d141f;min-height:105px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:7px;text-align:center}.homePartyMon img{width:58px;height:58px;object-fit:contain}.homePartyMon b{font-size:10px;max-width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.homePartyEmpty{color:#536178;font-size:11px;border-style:dashed}.homeToolGrid{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:14px}.homeTool{text-align:left;min-height:84px;background:#101925;border:1px solid #2b3a50;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:5px}.homeTool b{font-size:14px}.homeTool span{font-size:10px;color:#96a6bb;font-weight:600;line-height:1.35}.homeMetaTop{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:9px;margin-top:14px}.homeMetaMon{border:1px solid #2b3a50;background:#0e1521;border-radius:14px;padding:9px;text-align:center;cursor:pointer}.homeMetaMon:hover{background:#162236}.homeMetaMon img{width:60px;height:60px;object-fit:contain}.homeMetaMon b{display:block;font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.homeMetaRank{font-size:10px;color:#9fc0f4;font-weight:900}.homeStateRow{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}.homeStateChip{border:1px solid #33445d;background:#101925;border-radius:999px;padding:5px 8px;font-size:10px;color:#c7d4e5}
@media(max-width:1000px){.homeHeroV18,.homeGridV18{grid-template-columns:1fr}.homePartyPreview,.homeMetaTop{grid-template-columns:repeat(3,1fr)}}
@media(max-width:650px){.appnav{grid-template-columns:repeat(2,minmax(0,1fr))!important}.homePartyPreview,.homeMetaTop{grid-template-columns:repeat(2,1fr)}.homeToolGrid{grid-template-columns:1fr}.homeHeroV18{padding:16px}.homeSetupScore{font-size:42px}}
'''
style_marker = '</style>\n\n<style id="v17-web-shell">'
if style_marker not in s:
    raise SystemExit('style marker not found')
s = s.replace(style_marker, css + '\n</style>\n\n<style id="v17-web-shell">', 1)

s = s.replace('let currentPage="quick";', 'let currentPage="home";', 1)
s = s.replace("const order=['quick','saved','build','env'];", "const order=['home','quick','saved','build','env'];", 1)
s = s.replace(" if(p==='saved'){renderSavedEditors();renderSavedRoster();renderSavedCompletion()}", " if(p==='home'){renderHomeV18()}\n if(p==='saved'){renderSavedEditors();renderSavedRoster();renderSavedCompletion()}", 1)
s = s.replace(" currentPage=p;", " currentPage=p;\n try{localStorage.setItem('champ_last_page',p)}catch(e){}", 1)

home_js = r'''
/* ===== v18 useful dashboard logic ===== */
function homeTeamSourceV18(){
  if(Array.isArray(savedParty)&&savedParty.length)return savedParty;
  if(Array.isArray(mine)&&mine.length)return mine;
  if(Array.isArray(buildTeam)&&buildTeam.length)return buildTeam;
  return [];
}
function homePrimaryAction(){
  if(savedParty.length<6){switchPage('saved');return;}
  if(buildTeam.length<2){
    buildTeam=savedParty.map(x=>mons.find(m=>m.name===x.name)||x).filter(Boolean).slice(0,6);
    try{localStorage.setItem('champ_build',JSON.stringify(buildTeam))}catch(e){}
    switchPage('build');return;
  }
  homeUseSavedQuick();
}
function homeUseSavedQuick(){
  if(savedParty.length){loadSavedToQuick();return;}
  switchPage('quick');
}
function homeFocusCounter(){
  switchPage('build');
  setTimeout(()=>{const x=document.getElementById('counterPokemonInput');x?.focus();document.getElementById('counterTool')?.scrollIntoView({behavior:'smooth',block:'start'});},80);
}
function homeOpenEnvV18(index){
  switchPage('env');
  setTimeout(()=>showEnvByIndex(index),40);
}
function renderHomeV18(){
  const team=homeTeamSourceV18();
  const savedN=savedParty.length,buildN=buildTeam.length,mineN=mine.length;
  const setup=Math.round(Math.min(100,(savedN/6)*55+(buildN>=2?25:0)+(mineN>=3?20:0)));
  const score=document.getElementById('homeSetupScore'),bar=document.getElementById('homeSetupBar'),label=document.getElementById('homeSetupLabel');
  if(score)score.textContent=setup+'%';if(bar)bar.style.width=setup+'%';
  if(label)label.textContent=savedN===6?'パーティ登録済み':savedN?`登録 ${savedN}/6`:'まず6体を登録';

  const next=document.getElementById('homeNextText'),btn=document.getElementById('homePrimaryAction');
  if(savedN<6){if(next)next.innerHTML=`まず<b>自分の6体</b>を登録すると、構築分析とクイック選出を最短で使えます。現在 ${savedN}/6。`;if(btn)btn.textContent='6体を登録する →';}
  else if(buildN<2){if(next)next.innerHTML='登録パーティは完成。次は<b>構築分析</b>で弱点・役割不足・おすすめ補完を確認するのがおすすめです。';if(btn)btn.textContent='この6体を構築分析 →';}
  else {if(next)next.innerHTML='準備OK。対戦前は<b>クイック選出</b>、構築を変えたい時は<b>総合分析</b>を使えばすぐ進めます。';if(btn)btn.textContent='登録パーティで選出 →';}

  const preview=document.getElementById('homePartyPreview');
  if(preview){
    preview.innerHTML=Array.from({length:6},(_,i)=>{
      const raw=team[i],m=raw&&(mons.find(x=>x.name===raw.name)||raw);
      if(!m)return `<div class="homePartyEmpty">${i+1}</div>`;
      return `<div class="homePartyMon"><img src="${sprite(m)}" onerror="this.src='${fallback(m)}'"><b>${m.name}</b></div>`;
    }).join('');
  }
  const hint=document.getElementById('homePartyHint');
  if(hint)hint.innerHTML=`<div class="homeStateRow"><span class="homeStateChip">保存 ${savedN}/6</span><span class="homeStateChip">構築 ${buildN}/6</span><span class="homeStateChip">選出側 ${mineN}/6</span></div>`;

  const top=(mons||[]).filter(m=>m.usageRank&&m.usageRank<=150&&!m.mega).sort((a,b)=>a.usageRank-b.usageRank).slice(0,6);
  const meta=document.getElementById('homeMetaTop');
  if(meta)meta.innerHTML=top.map(m=>`<div class="homeMetaMon" onclick="homeOpenEnvV18(${mons.indexOf(m)})"><div class="homeMetaRank">#${m.usageRank}</div><img src="${sprite(m)}" onerror="this.src='${fallback(m)}'"><b>${m.name}</b><div>${typeChip(m.t1)}${typeChip(m.t2)}</div></div>`).join('');
}
'''
boot_marker = 'function safeBoot(name, fn){'
if boot_marker not in s:
    raise SystemExit('boot marker not found')
s = s.replace(boot_marker, home_js + '\n' + boot_marker, 1)
s = s.replace('safeBoot("選択表示", renderSelected);', 'safeBoot("ホーム", renderHomeV18);\nsafeBoot("選択表示", renderSelected);', 1)

p.write_text(s, encoding='utf-8')
print('applied v18 useful dashboard')
