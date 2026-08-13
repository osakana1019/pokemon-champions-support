from pathlib import Path
p=Path('index.html');s=p.read_text(encoding='utf-8')
if '/* v20.3 classic */' in s: raise SystemExit(0)
pos=s.find('/* ===== v20.2 original clean home ===== */')
if pos>=0:
 a=s.rfind('<style>',0,pos); b=s.find('<script>',pos); c=s.find('</script>',b)
 if min(a,b,c)>=0: s=s[:a]+s[c+9:]
s=s.replace('Pokémon Champions Support — v20.2','Pokémon Champions Support — v20.3')
old="T={charcoal:['チャコール','#252a31'],light:['ライト','#f8f9fa'],dark:['ダーク','#13171c'],teal:['ティール','#172625']}"
new="T={charcoal:['チャコール','#252a31'],classic:['クラシック','#111722'],light:['ライト','#f8f9fa'],dark:['ダーク','#13171c'],teal:['ティール','#172625']}"
s=s.replace(old,new,1)
css='''<style id="v203-classic">/* v20.3 classic */
html[data-app-theme=classic]{--xbg:#080b11;--xtop:#0c1220;--xcard:#111722;--xcard2:#0d141f;--xline:#2a3548;--xtext:#f7f8fb;--xmuted:#9aa7ba;--xsoft:#24324b;--xaccent:#6da7ff;--xaccenttext:#fff;color-scheme:dark}
html[data-app-theme=classic] body{background:linear-gradient(180deg,#0c1220,#080b11 42%)!important}
html[data-app-theme=classic] .primary,html[data-app-theme=classic] .mineAdd,html[data-app-theme=classic] .buildAddBtn,html[data-app-theme=classic] .appnav .activeApp{background:linear-gradient(135deg,#6da7ff,#9479ff)!important;color:#fff!important}
</style>'''
s=s.replace('</body>',css+'\n</body>',1);p.write_text(s,encoding='utf-8')
