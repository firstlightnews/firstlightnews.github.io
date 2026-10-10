import re,sys
D='/tmp/claude-0/-home-claude/9cb38d5d-e20b-54ed-9c6c-841e106873bb/scratchpad/'
src=open(sys.argv[1]).read(); out=sys.argv[2]; preview=len(sys.argv)>3
if preview: src=re.sub(r'<!-- Google tag.*?</script>\s*<script>.*?</script>','',src,flags=re.S)
assert 'uiToggle' not in src
css=open(D+'modern.css').read()+open(D+'plain.css').read()+open(D+'real.css').read()+open(D+'classic2.css').read()+open(D+'toggle.css').read()
# drop the old toggle rules from modern.css/plain.css (toggle.css replaces them)
css=re.sub(r'(?m)^.*\.uitoggle[^\n]*\n','',css.split('/* ===== edition toggle')[0])+'/* ===== edition toggle'+css.split('/* ===== edition toggle')[1]
css=css.replace('@media (max-width:640px){header h1{padding-right:0}}','')
PAPER=open(D+'paper16.svg').read().replace(' width="32" height="32"','')
STAMP='''<svg viewBox="-6 -6 232 108" width="100%" height="100%" aria-hidden="true"><defs><filter id="fln-ink"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 1.6"/><feComposite in="SourceGraphic" operator="in"/></filter></defs><g filter="url(#fln-ink)" fill="none" stroke="#c4161c"><rect x="5" y="5" width="210" height="86" rx="6" stroke-width="5"/><rect x="13" y="13" width="194" height="70" rx="3" stroke-width="2"/><text x="110" y="42" text-anchor="middle" font-family="Georgia,serif" font-weight="bold" font-size="15" letter-spacing="3" fill="#c4161c" stroke="none">NOW AVAILABLE</text><text x="110" y="74" text-anchor="middle" font-family="Georgia,serif" font-weight="bold" font-size="32" textLength="176" lengthAdjust="spacingAndGlyphs" fill="#c4161c" stroke="none">ONLINE</text></g></svg>'''
BTN=f'<button class="uitoggle" id="uiToggle" type="button" aria-label="Read the print edition"><span class="tg-retro"><span class="new">NEW!</span>{PAPER}<span>Print Edition</span></span><span class="tg-print">{STAMP}</span></button>\n    '
HEAD='''<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Old+Standard+TT:ital,wght@0,400;0,700;1,400&family=PT+Serif:ital,wght@0,400;0,700;1,400&family=UnifrakturMaguntia&display=swap">
<script>try{if(localStorage.getItem("fln-ui")==="print")document.documentElement.classList.add("modern")}catch(e){}</script>
'''
JS='''/* ---------- edition toggle ---------- */
(function(){const b=$("uiToggle"),h=document.documentElement;
 const ed=()=>{const L=Date.UTC(2026,9,9),d=new Date(new Date().toLocaleString("en-US",{timeZone:"America/New_York"}));return Math.max(1,Math.round((Date.UTC(d.getFullYear(),d.getMonth(),d.getDate())-L)/864e5)+1)};
 const roman=n=>{const m=[[1000,"M"],[900,"CM"],[500,"D"],[400,"CD"],[100,"C"],[90,"XC"],[50,"L"],[40,"XL"],[10,"X"],[9,"IX"],[5,"V"],[4,"IV"],[1,"I"]];let r="";for(const[v,s]of m)while(n>=v){r+=s;n-=v}return r};
 const vol=()=>{const d=new Date(new Date().toLocaleString("en-US",{timeZone:"America/New_York"}));let y=d.getFullYear()-2026;if(d.getMonth()<9||(d.getMonth()===9&&d.getDate()<9))y--;return roman(Math.max(1,y+1))};
 const dl=document.querySelector(".dateline");dl.setAttribute("data-vol",vol());dl.setAttribute("data-ed",ed());
 window.setEdition=(e)=>{if(e&&e.no)dl.setAttribute("data-ed",String(e.no));};
 const sync=()=>{const m=h.classList.contains("modern");b.setAttribute("aria-label",m?"Back to the original online edition":"Read the print edition");};
 b.addEventListener("click",()=>{h.classList.toggle("modern");store("fln-ui",h.classList.contains("modern")?"print":"original");sync();window.scrollTo(0,0);});sync();})();
'''
i=src.index('</style>',src.index('/* Layout: late-90s'))
src=src[:i]+css+src[i:]
src=src.replace('<title>',HEAD+'<title>',1)
assert '<header>\n    <h1>' in src
src=src.replace('<header>\n    <h1>','<header>\n    '+BTN+'<h1>',1)
JS2='''(function(){const st=$("stories"),bn=$("banner");const sync=()=>{const f=st.querySelector(".story");bn.replaceChildren(f?f.cloneNode(true):"");};new MutationObserver(sync).observe(st,{childList:true});sync();})();
document.querySelectorAll(".turn").forEach(a=>a.addEventListener("click",()=>{showTab(a.dataset.to);window.scrollTo(0,0);}));\n'''
k=src.index('$("today").textContent'); src=src[:k]+JS+src[k:]
src=src.replace('<div class="overview" id="overview" hidden></div>','<div class="banner" id="banner" aria-hidden="true"></div>\n    <div class="overview" id="overview" hidden></div>',1)
assert 'id="banner"' in src
src=src.replace('\n  </section>\n\n  <section class="panel" id="p-reading"','\n    <a class="turn" data-to="reading" role="button" tabindex="0">Continued on Page 2</a>\n  </section>\n\n  <section class="panel" id="p-reading"',1)
src=src.replace('\n  </section>\n\n  <section class="panel" id="p-sports"','\n    <a class="turn" data-to="sports" role="button" tabindex="0">Sports on Page 3</a>\n  </section>\n\n  <section class="panel" id="p-sports"',1)
assert src.count('class="turn"')==2, src.count('class="turn"')
j=src.rindex('</script>'); src=src[:j]+JS2+src[j:]
src=src.replace('<div id="stories">','<div id="stories" data-x>',1)
if preview:
    ff='<style>@font-face{font-family:"PT Serif";src:url(pt-serif-latin-400-normal.woff2)}@font-face{font-family:"PT Serif";src:url(pt-serif-latin-400-italic.woff2);font-style:italic}@font-face{font-family:"PT Serif";src:url(pt-serif-latin-700-normal.woff2);font-weight:700}@font-face{font-family:Georgia;src:url(gelasio-latin-400-normal.woff2);font-weight:400}@font-face{font-family:Georgia;src:url(gelasio-latin-700-normal.woff2);font-weight:700 900}@font-face{font-family:Georgia;src:url(gelasio-latin-400-italic.woff2);font-style:italic}@font-face{font-family:"UnifrakturMaguntia";src:url(unifrakturmaguntia-latin-400-normal.woff2)}@font-face{font-family:"Old Standard TT";src:url(old-standard-tt-latin-400-normal.woff2)}@font-face{font-family:"Old Standard TT";src:url(old-standard-tt-latin-700-normal.woff2);font-weight:700}@font-face{font-family:"Old Standard TT";src:url(old-standard-tt-latin-400-italic.woff2);font-style:italic}</style>\n'
    src=src.replace('<title>',ff+'<title>',1)
open(out,'w').write(src); print('built',out,len(src))
