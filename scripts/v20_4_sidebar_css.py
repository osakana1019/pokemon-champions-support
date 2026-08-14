from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8')
marker='/* ===== v20.7 reliable rail glyphs ===== */'
if marker in s: raise SystemExit(0)
s=s.replace('Pokémon Champions Support — v20.6','Pokémon Champions Support — v20.7')
s=s.replace('<div class="badge">v20.6</div>','<div class="badge">v20.7</div>',1)
css=r'''<style id="v207-rail-glyphs">
/* ===== v20.7 reliable rail glyphs ===== */
@media(min-width:1080px){
 #v205Rail .v205RailBtn svg{display:none!important}
 #v205Rail .v205RailBtn{overflow:visible!important;color:var(--xmuted)!important}
 #v205Rail .v205RailBtn:hover{color:var(--xtext)!important}
 #v205Rail .v205RailBtn.active{color:var(--xaccenttext)!important}
 .v207Glyph{position:relative;display:block!important;width:24px;height:24px;flex:0 0 24px;color:currentColor;pointer-events:none}
 .v207-home:before{content:'';position:absolute;left:5px;bottom:3px;width:14px;height:12px;border:2px solid currentColor;border-top:0;border-radius:2px}
 .v207-home:after{content:'';position:absolute;left:6px;top:3px;width:12px;height:12px;border-left:2px solid currentColor;border-top:2px solid currentColor;transform:rotate(45deg);border-radius:1px}
 .v207-quick:before{content:'';position:absolute;inset:2px 5px;background:currentColor;clip-path:polygon(58% 0,15% 54%,45% 54%,31% 100%,86% 42%,55% 42%)}
 .v207-party:before{content:'';position:absolute;left:4px;top:3px;width:6px;height:6px;border-radius:50%;background:currentColor;box-shadow:10px 0 0 currentColor}
 .v207-party:after{content:'';position:absolute;left:2px;bottom:3px;width:20px;height:9px;border:2px solid currentColor;border-bottom:0;border-radius:12px 12px 3px 3px}
 .v207-env:before{content:'';position:absolute;left:3px;bottom:3px;width:4px;height:10px;border-radius:2px 2px 0 0;background:currentColor;box-shadow:7px -6px 0 currentColor,14px -2px 0 currentColor}
 .v207-env:after{content:'';position:absolute;left:2px;right:1px;bottom:2px;height:2px;border-radius:2px;background:currentColor}
 .v207-settings:before{content:'';position:absolute;left:2px;right:2px;top:5px;height:2px;background:currentColor;box-shadow:0 6px 0 currentColor,0 12px 0 currentColor}
 .v207-settings:after{content:'';position:absolute;left:6px;top:2px;width:5px;height:5px;border:2px solid currentColor;border-radius:50%;background:var(--xcard);box-shadow:8px 6px 0 -1px var(--xcard),8px 6px 0 1px currentColor,2px 12px 0 -1px var(--xcard),2px 12px 0 1px currentColor}
 .v205Tip{pointer-events:none!important;visibility:hidden!important;opacity:0!important}
 .v205RailBtn:hover .v205Tip{visibility:visible!important;opacity:1!important}
}
</style>'''
s=s.replace('</body>',css+'\n</body>',1);p.write_text(s,encoding='utf-8')
