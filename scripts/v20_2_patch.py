from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8')
marker='/* ===== v20.2 theme settings ===== */'
if marker in s: raise SystemExit(0)
s=s.replace('Pokémon Champions Support — v20.1','Pokémon Champions Support — v20.2')
s=s.replace('const sprite=m=>v201PixelSprite(m);',"const v202ClearSprite=m=>`https://play.pokemonshowdown.com/sprites/home-centered/${v201PixelSlug(m)}.png`;\nconst sprite=m=>v202ClearSprite(m);",1)
s=s.replace('const fallback=m=>V201_PIXEL_PLACEHOLDER;','const fallback=m=>specialMegaArt[m.name]||homeSprite(m)||V201_PIXEL_PLACEHOLDER;',1)
patch=r'''
<style id="v202-theme">
/* ===== v20.2 theme settings ===== */
html[data-app-theme=charcoal]{--xbg:#171a1f;--xtop:#20242a;--xcard:#252a31;--xcard2:#2b3038;--xline:#3d444e;--xtext:#eef1f4;--xmuted:#aab2bd;--xsoft:#30363e;--xaccent:#e7eaee;--xaccenttext:#171a1f}
html[data-app-theme=light]{--xbg:#e9ebee;--xtop:#f0f2f4;--xcard:#f8f9fa;--xcard2:#f1f3f5;--xline:#cbd0d7;--xtext:#252a31;--xmuted:#69717d;--xsoft:#e3e6ea;--xaccent:#24282f;--xaccenttext:#fff}
html[data-app-theme=dark]{--xbg:#090b0e;--xtop:#0f1216;--xcard:#13171c;--xcard2:#181d23;--xline:#2a3038;--xtext:#e8ebef;--xmuted:#8f98a4;--xsoft:#1d232a;--xaccent:#f1f3f5;--xaccenttext:#0b0d10}
html[data-app-theme=teal]{--xbg:#0d1717;--xtop:#122020;--xcard:#172625;--xcard2:#1d2e2c;--xline:#35504c;--xtext:#edf7f5;--xmuted:#9eb7b2;--xsoft:#203532;--xaccent:#71dbc3;--xaccenttext:#0b1a17}
html[data-app-theme]{background:var(--xbg)!important;color-scheme:dark}html[data-app-theme=light]{color-scheme:light}
html[data-app-theme] body{background:linear-gradient(180deg,var(--xtop),var(--xbg) 240px)!important;color:var(--xtext)!important}
html[data-app-theme] .card,html[data-app-theme] .teamPane,html[data-app-theme] .savedEditor,html[data-app-theme] .counterToolCard,html[data-app-theme] .pick,html[data-app-theme] .metaRec,html[data-app-theme] .v12BuildPick,html[data-app-theme] .v19IntelCard,html[data-app-theme] .v19Mini,html[data-app-theme] .v19TeamSpeed{background:var(--xcard)!important;border-color:var(--xline)!important;color:var(--xtext)!important}
html[data-app-theme] .small,html[data-app-theme] .sub,html[data-app-theme] .buildReasons{color:var(--xmuted)!important}
html[data-app-theme] .mon,html[data-app-theme] .sel,html[data-app-theme] .rankRow,html[data-app-theme] .oppQuickMon,html[data-app-theme] .savedEmpty,html[data-app-theme] .dataSection,html[data-app-theme] .typeMatchSection{background:var(--xcard2)!important;border-color:var(--xline)!important;color:var(--xtext)!important}
html[data-app-theme] input,html[data-app-theme] select,html[data-app-theme] textarea,html[data-app-theme] .savedItem,html[data-app-theme] .buildItemInput,html[data-app-theme] .buildMoveInput{background:var(--xcard2)!important;border-color:var(--xline)!important;color:var(--xtext)!important}
html[data-app-theme] button{background:var(--xsoft)!important;color:var(--xtext)!important;box-shadow:inset 0 0 0 1px var(--xline)!important}html[data-app-theme] .primary,html[data-app-theme] .mineAdd,html[data-app-theme] .buildAddBtn{background:var(--xaccent)!important;color:var(--xaccenttext)!important;box-shadow:none!important}
html[data-app-theme] .appnav{background:var(--xcard)!important}html[data-app-theme] .appnav button{background:transparent!important;color:var(--xmuted)!important;box-shadow:none!important}html[data-app-theme] .appnav .activeApp{background:var(--xaccent)!important;color:var(--xaccenttext)!important}
html[data-app-theme] .moveSuggestBox,html[data-app-theme] .buildMoveSuggestBox,html[data-app-theme] .itemSuggestBox,html[data-app-theme] .counterSuggestBoxV186{background:var(--xcard)!important;border-color:var(--xline)!important;color:var(--xtext)!important}
.mon img,.sel img,.rankRow img,.oppQuickMon img,.profile img,.pick img,.metaRec img,.savedHead img,.homePartyMon img,.homeMetaMon img{image-rendering:auto!important;filter:none!important}
#v202SettingsBtn{position:fixed;right:16px;bottom:16px;z-index:490;border-radius:999px!important;padding:9px 14px!important;background:var(--xcard)!important;color:var(--xtext)!important;border:1px solid var(--xline)!important}#v202SettingsPanel{position:fixed;right:16px;bottom:68px;z-index:495;width:min(350px,calc(100vw - 28px));padding:14px;border-radius:18px;background:var(--xcard)!important;color:var(--xtext)!important;border:1px solid var(--xline)!important;box-shadow:0 18px 48px #0004;display:none}#v202SettingsPanel.show{display:block}.v202ThemeGrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.v202ThemeGrid button{text-align:left!important}.v202ThemeGrid button.active{outline:2px solid var(--xaccent)}.v202Swatch{display:block;height:24px;border-radius:7px;margin-bottom:5px;border:1px solid var(--xline)}
</style>
<script>
(function(){const K='champ_ui_theme_v202',T={charcoal:['チャコール','#252a31'],light:['ライト','#f8f9fa'],dark:['ダーク','#13171c'],teal:['ティール','#172625']};function set(k,save=true){if(!T[k])k='charcoal';document.documentElement.dataset.appTheme=k;if(save)try{localStorage.setItem(K,k)}catch(e){};document.querySelectorAll('.v202ThemeGrid button').forEach(b=>b.classList.toggle('active',b.dataset.t===k))}let cur='charcoal';try{cur=localStorage.getItem(K)||cur}catch(e){};set(cur,false);const b=document.createElement('button');b.id='v202SettingsBtn';b.textContent='設定';const p=document.createElement('div');p.id='v202SettingsPanel';p.innerHTML='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px"><b>表示設定</b><button data-close>×</button></div><div class="small" style="margin-bottom:7px">テーマ</div><div class="v202ThemeGrid">'+Object.entries(T).map(([k,v])=>`<button data-t="${k}"><span class="v202Swatch" style="background:${v[1]}"></span><b>${v[0]}</b></button>`).join('')+'</div>';document.body.append(p,b);b.onclick=()=>p.classList.toggle('show');p.querySelector('[data-close]').onclick=()=>p.classList.remove('show');p.querySelectorAll('[data-t]').forEach(x=>x.onclick=()=>set(x.dataset.t));set(cur,false);window.v202SetTheme=set;})();
</script>
'''
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
