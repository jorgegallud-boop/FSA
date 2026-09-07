import json, os

BASE = os.path.dirname(__file__)

with open(os.path.join(BASE, "..", "data", "deck_data.json"), encoding="utf-8") as f:
    deck_json = f.read()

CSS = """
<title>Financial Statement Analysis</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,500;0,600;1,500&family=Public+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
  :root{
    --ink:#1c2320;
    --ink-soft:#4b5650;
    --paper:#eef1ef;
    --surface:#ffffff;
    --rule:#c7d0cb;
    --rule-strong:#a9b6b0;
    --accent:#0f6b57;
    --accent-soft:#dbe9e4;
    --flag:#a8752c;
    --shadow: 0 1px 2px rgba(28,35,32,.06), 0 8px 24px rgba(28,35,32,.05);
  }
  @media (prefers-color-scheme: dark){
    :root:not([data-theme="light"]){
      --ink:#e8ece9;
      --ink-soft:#a8b3ac;
      --paper:#101513;
      --surface:#182420;
      --rule:#2b3733;
      --rule-strong:#3c4a44;
      --accent:#4fd0ab;
      --accent-soft:#1d332c;
      --flag:#d9a55a;
      --shadow: 0 1px 2px rgba(0,0,0,.4), 0 8px 28px rgba(0,0,0,.35);
    }
  }
  :root[data-theme="dark"]{
    --ink:#e8ece9;
    --ink-soft:#a8b3ac;
    --paper:#101513;
    --surface:#182420;
    --rule:#2b3733;
    --rule-strong:#3c4a44;
    --accent:#4fd0ab;
    --accent-soft:#1d332c;
    --flag:#d9a55a;
    --shadow: 0 1px 2px rgba(0,0,0,.4), 0 8px 28px rgba(0,0,0,.35);
  }

  *{box-sizing:border-box;}
  body{
    background:var(--paper);
    color:var(--ink);
    font-family:"Public Sans", ui-sans-serif, system-ui, sans-serif;
    -webkit-font-smoothing:antialiased;
  }
  #app{min-height:100vh;}
  a{color:inherit;}
  .mono{font-family:"IBM Plex Mono", ui-monospace, monospace; font-variant-numeric:tabular-nums;}
  .serif{font-family:"Newsreader", Georgia, serif;}

  /* ---------- INDEX ---------- */
  .index-wrap{
    max-width:760px;
    margin:0 auto;
    padding:clamp(28px,6vw,72px) 20px 80px;
  }
  .masthead{
    border-bottom:2px solid var(--ink);
    padding-bottom:20px;
    margin-bottom:8px;
  }
  .kicker{
    font-family:"IBM Plex Mono", monospace;
    font-size:12px;
    letter-spacing:.12em;
    text-transform:uppercase;
    color:var(--accent);
    margin:0 0 10px;
  }
  .masthead h1{
    font-family:"Newsreader", Georgia, serif;
    font-weight:600;
    font-size:clamp(30px,5.2vw,46px);
    line-height:1.08;
    margin:0 0 12px;
    text-wrap:balance;
  }
  .masthead p{
    margin:0;
    color:var(--ink-soft);
    font-size:15px;
    max-width:56ch;
  }
  .toc{
    list-style:none;
    margin:0;
    padding:0;
  }
  .toc-row{
    display:grid;
    grid-template-columns:52px 1fr auto auto;
    align-items:baseline;
    gap:18px;
    padding:22px 4px;
    border-bottom:1px solid var(--rule);
    cursor:pointer;
    text-decoration:none;
    color:inherit;
    transition:background .12s ease;
  }
  .toc-row:first-child{border-top:1px solid var(--rule);}
  .toc-row:hover{background:var(--accent-soft);}
  .toc-row:hover .toc-name{color:var(--accent);}
  .toc-num{
    font-family:"IBM Plex Mono", monospace;
    font-size:13px;
    color:var(--ink-soft);
  }
  .toc-body{min-width:0;}
  .toc-name{
    font-family:"Newsreader", Georgia, serif;
    font-size:clamp(19px,2.6vw,24px);
    font-weight:500;
    display:block;
    transition:color .12s ease;
  }
  .toc-sub{
    display:block;
    font-size:13px;
    color:var(--ink-soft);
    margin-top:3px;
  }
  .toc-count{
    font-family:"IBM Plex Mono", monospace;
    font-size:13px;
    color:var(--ink-soft);
    white-space:nowrap;
  }
  .toc-go{
    font-family:"IBM Plex Mono", monospace;
    font-size:13px;
    color:var(--accent);
    white-space:nowrap;
  }
  .index-foot{
    margin-top:28px;
    font-size:12.5px;
    color:var(--ink-soft);
    display:flex;
    justify-content:space-between;
    gap:12px;
    flex-wrap:wrap;
  }
  @media (max-width:480px){
    .toc-row{grid-template-columns:34px 1fr;}
    .toc-count{display:none;}
    .toc-go{grid-column:2; justify-self:start; margin-top:6px;}
  }

  /* ---------- DECK ---------- */
  .deck{
    min-height:100vh;
    display:flex;
    flex-direction:column;
  }
  .deck-bar{
    display:flex;
    align-items:center;
    gap:14px;
    padding:14px 20px;
    border-bottom:1px solid var(--rule);
    background:var(--surface);
    position:sticky; top:0; z-index:5;
  }
  .back-link{
    font-family:"IBM Plex Mono", monospace;
    font-size:13px;
    text-decoration:none;
    color:var(--ink-soft);
    display:flex; align-items:center; gap:6px;
    padding:4px 2px;
  }
  .back-link:hover{color:var(--accent);}
  .deck-title{
    font-family:"Newsreader", Georgia, serif;
    font-size:15px;
    font-weight:600;
    color:var(--ink-soft);
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
  }
  .deck-pos{
    margin-left:auto;
    font-family:"IBM Plex Mono", monospace;
    font-size:13px;
    color:var(--ink-soft);
    white-space:nowrap;
  }
  .progress-rule{
    height:2px;
    background:var(--rule);
  }
  .progress-fill{
    height:100%;
    background:var(--accent);
    transition:width .18s ease;
  }
  .stage-wrap{
    flex:1;
    position:relative;
    display:flex;
  }
  .tap-zone{
    position:absolute; top:0; bottom:0; width:18%; z-index:3;
    cursor:pointer;
  }
  .tap-zone.left{left:0;}
  .tap-zone.right{right:0;}
  .stage{
    flex:1;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:48px 24px 100px;
    overflow-y:auto;
  }
  .slide{
    width:100%;
    max-width:760px;
  }
  .slide h2{
    font-family:"Newsreader", Georgia, serif;
    font-weight:600;
    font-size:clamp(24px,4vw,34px);
    margin:0 0 22px;
    text-wrap:balance;
    border-bottom:2px solid var(--ink);
    padding-bottom:14px;
  }
  .slide.is-divider{
    text-align:center;
    max-width:640px;
  }
  .slide.is-divider .divider-title{
    font-family:"Newsreader", Georgia, serif;
    font-weight:600;
    font-size:clamp(30px,6vw,52px);
    line-height:1.12;
    margin:0 0 14px;
    text-wrap:balance;
  }
  .slide.is-divider .divider-rule{
    width:64px; height:3px; background:var(--accent);
    margin:0 auto 18px;
  }
  .slide.is-divider .divider-sub{
    font-size:16px; color:var(--ink-soft);
  }
  .bullets{
    list-style:none;
    margin:0; padding:0;
    display:flex; flex-direction:column; gap:10px;
  }
  .bullets li{
    font-size:17px;
    line-height:1.5;
    padding-left:22px;
    position:relative;
  }
  .bullets li::before{
    content:"—";
    position:absolute; left:0; top:0;
    color:var(--accent);
  }
  .bullets li[data-level="1"]{
    margin-left:26px;
    font-size:15.5px;
    color:var(--ink-soft);
  }
  .bullets li[data-level="1"]::before{content:"·"; font-size:20px; top:-3px;}
  .bullets li[data-level="2"]{margin-left:50px; font-size:14.5px;}
  .aside-note{
    margin-top:18px;
    font-size:12.5px;
    font-family:"IBM Plex Mono", monospace;
    color:var(--flag);
    border:1px dashed var(--flag);
    display:inline-block;
    padding:4px 9px;
    border-radius:3px;
  }
  .tbl-wrap{
    overflow-x:auto;
    margin-top:6px;
    border:1px solid var(--rule-strong);
  }
  table.ledger{
    border-collapse:collapse;
    width:100%;
    font-size:14.5px;
  }
  table.ledger td{
    padding:8px 12px;
    border-bottom:1px solid var(--rule);
    border-right:1px solid var(--rule);
    vertical-align:top;
    white-space:pre-line;
  }
  table.ledger tr:first-child td{
    font-family:"IBM Plex Mono", monospace;
    font-size:12px;
    letter-spacing:.03em;
    text-transform:uppercase;
    color:var(--ink-soft);
    background:var(--accent-soft);
  }
  table.ledger td:last-child{border-right:none;}
  table.ledger tr:last-child td{border-bottom:none;}
  table.ledger td.num{
    font-family:"IBM Plex Mono", monospace;
    text-align:right;
    font-variant-numeric:tabular-nums;
  }
  figure.slide-img{
    margin:0; text-align:center;
  }
  figure.slide-img img{
    max-width:100%;
    max-height:56vh;
    border:1px solid var(--rule-strong);
    cursor:zoom-in;
    background:var(--surface);
  }
  figure.slide-img figcaption{
    margin-top:8px;
    font-size:12px;
    color:var(--ink-soft);
    font-family:"IBM Plex Mono", monospace;
  }
  .content-body{
    display:flex; flex-direction:column; gap:22px;
  }
  .deck-controls{
    position:sticky; bottom:0;
    display:flex; align-items:center; justify-content:center; gap:16px;
    padding:14px;
    background:linear-gradient(to top, var(--paper) 60%, transparent);
    z-index:4;
  }
  .ctrl-btn{
    font-family:"IBM Plex Mono", monospace;
    font-size:13px;
    background:var(--surface);
    border:1px solid var(--rule-strong);
    color:var(--ink);
    padding:9px 16px;
    border-radius:3px;
    cursor:pointer;
    box-shadow:var(--shadow);
  }
  .ctrl-btn:hover{border-color:var(--accent); color:var(--accent);}
  .ctrl-btn:disabled{opacity:.35; cursor:default;}
  .ctrl-btn:disabled:hover{border-color:var(--rule-strong); color:var(--ink);}

  .lightbox{
    position:fixed; inset:0; background:rgba(10,14,12,.86);
    display:flex; align-items:center; justify-content:center;
    padding:5vh 5vw;
    z-index:50; cursor:zoom-out;
  }
  .lightbox img{max-width:100%; max-height:100%;}
  [hidden]{display:none !important;}

  @media (prefers-reduced-motion: reduce){
    *{transition:none !important;}
  }
</style>
"""

HTML_BODY = """
<div id="app"></div>
<script type="application/json" id="deck-data">__DECK_JSON__</script>
<script>
(function(){
  var DATA = JSON.parse(document.getElementById('deck-data').textContent);
  var ORDER = ["unit1","unit2","unit3","unit4"];
  var app = document.getElementById('app');

  function esc(s){
    return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  }
  function nl2br(s){ return esc(s).replace(/\\n/g,"<br>"); }
  function looksNumeric(s){
    var t = (s||"").trim();
    if(!t) return false;
    return /^[\\-\\(]?[\\d.,%\\s]+\\)?$/.test(t) && /\\d/.test(t);
  }

  function renderIndex(){
    var rows = ORDER.map(function(key, i){
      var u = DATA[key];
      return '<a class="toc-row" href="#/'+key+'/1">' +
        '<span class="toc-num mono">'+String(i+1).padStart(2,'0')+'</span>' +
        '<span class="toc-body"><span class="toc-name">'+esc(u.unit)+' — '+esc(u.name)+'</span>' +
          '<span class="toc-sub">'+u.slides.length+' slides</span></span>' +
        '<span class="toc-count mono">'+u.slides.length+'</span>' +
        '<span class="toc-go">Open →</span>' +
      '</a>';
    }).join("");

    app.innerHTML =
      '<div class="index-wrap">' +
        '<div class="masthead">' +
          '<p class="kicker">Financial Statement Analysis</p>' +
          '<h1>Course slides</h1>' +
          '<p>The four units of the course, in web format. Navigate with the keyboard arrows, by tapping the sides, or with the buttons at the bottom. This site will be updated as the course progresses.</p>' +
        '</div>' +
        '<ul class="toc" style="list-style:none;padding:0;margin:0;">' + rows + '</ul>' +
        '<div class="index-foot"><span>jorge.gallud@uva.es</span><span>University of Valladolid</span></div>' +
      '</div>';
  }

  function slideInner(slide){
    if(slide.isTitle){
      return '<div class="slide is-divider">' +
        '<div class="divider-title">'+nl2br(slide.title)+'</div>' +
        '<div class="divider-rule"></div>' +
        (slide.subtitle ? '<div class="divider-sub">'+nl2br(slide.subtitle)+'</div>' : '') +
      '</div>';
    }
    var parts = [];
    if(slide.title) parts.push('<h2>'+esc(slide.title)+'</h2>');
    parts.push('<div class="content-body">');

    if(slide.bullets && slide.bullets.length){
      parts.push('<ul class="bullets">' + slide.bullets.map(function(b){
        return '<li data-level="'+b.level+'">'+esc(b.text)+'</li>';
      }).join("") + '</ul>');
    }

    (slide.tables||[]).forEach(function(tbl){
      var rows = tbl.map(function(row, ri){
        var cells = row.map(function(c){
          var cls = (ri>0 && looksNumeric(c.text)) ? ' class="num"' : '';
          var attrs = '';
          if(c.colspan>1) attrs += ' colspan="'+c.colspan+'"';
          if(c.rowspan>1) attrs += ' rowspan="'+c.rowspan+'"';
          return '<td'+cls+attrs+'>'+nl2br(c.text)+'</td>';
        }).join("");
        return '<tr>'+cells+'</tr>';
      }).join("");
      parts.push('<div class="tbl-wrap"><table class="ledger">'+rows+'</table></div>');
    });

    (slide.images||[]).forEach(function(img){
      parts.push('<figure class="slide-img"><img src="'+img.src+'" alt="" onclick="window.__zoom(this.src)"></figure>');
    });

    if(slide.asides && slide.asides.length){
      slide.asides.forEach(function(a){
        parts.push('<span class="aside-note">'+esc(a)+'</span>');
      });
    }

    parts.push('</div>');
    return '<div class="slide">' + parts.join("") + '</div>';
  }

  var state = {key:null, idx:0};

  function renderDeck(key, idx){
    var u = DATA[key];
    if(!u) return renderIndex();
    idx = Math.max(0, Math.min(idx, u.slides.length-1));
    state.key = key; state.idx = idx;
    var slide = u.slides[idx];
    var total = u.slides.length;
    var pct = Math.round(((idx+1)/total)*100);

    app.innerHTML =
      '<div class="deck">' +
        '<div class="deck-bar">' +
          '<a class="back-link" href="#/">← Index</a>' +
          '<span class="deck-title serif">'+esc(u.unit)+' — '+esc(u.name)+'</span>' +
          '<span class="deck-pos mono">'+(idx+1)+' / '+total+'</span>' +
        '</div>' +
        '<div class="progress-rule"><div class="progress-fill" style="width:'+pct+'%"></div></div>' +
        '<div class="stage-wrap">' +
          '<div class="tap-zone left" onclick="window.__nav(-1)"></div>' +
          '<div class="stage" id="stage">'+ slideInner(slide) +'</div>' +
          '<div class="tap-zone right" onclick="window.__nav(1)"></div>' +
        '</div>' +
        '<div class="deck-controls">' +
          '<button class="ctrl-btn" onclick="window.__nav(-1)" '+(idx===0?'disabled':'')+'>← Prev</button>' +
          '<button class="ctrl-btn" onclick="window.__nav(1)" '+(idx===total-1?'disabled':'')+'>Next →</button>' +
        '</div>' +
      '</div>';
    document.getElementById('stage').scrollTop = 0;
  }

  window.__nav = function(delta){
    if(!state.key) return;
    var u = DATA[state.key];
    var next = state.idx + delta;
    if(next<0 || next>=u.slides.length) return;
    location.hash = '#/'+state.key+'/'+(next+1);
  };
  window.__zoom = function(src){
    var box = document.createElement('div');
    box.className = 'lightbox';
    box.innerHTML = '<img src="'+src+'">';
    box.onclick = function(){ box.remove(); };
    document.body.appendChild(box);
  };

  function route(){
    var h = location.hash.replace(/^#\\/?/, '');
    if(!h){ renderIndex(); return; }
    var parts = h.split('/');
    var key = parts[0];
    var idx = (parseInt(parts[1],10) || 1) - 1;
    if(DATA[key]) renderDeck(key, idx);
    else renderIndex();
  }

  window.addEventListener('hashchange', route);
  document.addEventListener('keydown', function(e){
    var lb = document.querySelector('.lightbox');
    if(lb){ if(e.key==='Escape') lb.remove(); return; }
    if(!state.key) return;
    if(e.key==='ArrowRight' || e.key===' ') window.__nav(1);
    if(e.key==='ArrowLeft') window.__nav(-1);
  });

  route();
})();
</script>
"""

html = CSS + HTML_BODY.replace("__DECK_JSON__", deck_json)

out = os.path.join(BASE, "..", "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

import os
print("size MB:", os.path.getsize(out)/1024/1024)
