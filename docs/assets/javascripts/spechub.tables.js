(function(){
  'use strict';
  function $(sel, root){return (root||document).querySelector(sel);} 
  function $all(sel, root){return Array.from((root||document).querySelectorAll(sel));}
  function slug(s){return (s||'').toString().trim().toLowerCase().replace(/[^a-z0-9_\-\/:.]+/g,'-');}
  function parseHashQuery(){
    var h = location.hash||'';
    var q = h.startsWith('#?') ? h.slice(2) : (h.includes('#?') ? h.split('#?')[1] : '');
    var out = {};
    if(!q) return out;
    q.split('&').forEach(function(p){
      var kv = p.split('=');
      if(!kv[0]) return; var k = decodeURIComponent(kv[0]);
      var v = decodeURIComponent((kv[1]||'').replace(/\+/g,' '));
      if(!v) return; out[k] = v.split(',').map(function(x){return slug(x);});
    });
    return out;
  }
  function applyFilters(tbl, filters, searchValue){
    var rows = $all('tbody tr', tbl); var visible=0;
    var q = slug(searchValue||'');
    rows.forEach(function(tr){
      var ok = true;
      // AND across params
      Object.keys(filters).forEach(function(k){
        var want = filters[k]; if(!want || !want.length) return;
        var have = (tr.getAttribute('data-'+k)||'').split(/\s+/).filter(Boolean);
        // OR within param
        var hit = want.some(function(v){return have.includes(slug(v));});
        if(!hit) ok=false;
      });
      if(ok && q){
        var txt = slug(tr.textContent||'');
        if(txt.indexOf(q) === -1) ok=false;
      }
      tr.style.display = ok ? '' : 'none';
      if(ok) visible++;
    });
    var live = $('#live-'+tbl.id); if(live){ live.textContent = 'Rows: '+visible; }
  }
  function sortTable(tbl, colIdx, type, dir){
    var tbody = $('tbody', tbl); if(!tbody) return;
    var rows = $all('tr', tbody);
    var getText = function(td){return (td.textContent||'').trim();};
    rows.sort(function(a,b){
      var ta = a.cells[colIdx] ? getText(a.cells[colIdx]) : '';
      var tb = b.cells[colIdx] ? getText(b.cells[colIdx]) : '';
      var res;
      if(type==='number'){
        res = (parseFloat(ta)||0) - (parseFloat(tb)||0);
      } else {
        res = ta.localeCompare(tb);
      }
      return dir==='asc' ? res : -res;
    });
    rows.forEach(function(r){tbody.appendChild(r);});
    // aria-sort
    $all('th', tbl).forEach(function(th){ th.setAttribute('aria-sort','none'); th.removeAttribute('data-sort'); });
    var th = $all('th', tbl)[colIdx]; if(th){ th.setAttribute('aria-sort', dir==='asc'?'ascending':'descending'); th.setAttribute('data-sort', dir); }
  }
  function attachTable(tbl){
    var thead = $('thead', tbl); if(!thead) return;
    var ths = $all('th', thead);
    ths.forEach(function(th, idx){
      th.addEventListener('click', function(){
        var type = th.getAttribute('data-type')||'text';
        var cur = th.getAttribute('aria-sort');
        var next = cur==='ascending' ? 'desc' : 'asc';
        sortTable(tbl, idx, type, next);
      });
      th.addEventListener('keydown', function(e){ if(e.key==='Enter' || e.key===' '){ e.preventDefault(); th.click(); }});
    });
    // Filters
    var fid = 'filter-'+tbl.id; var cid = 'clear-'+tbl.id; var eid = 'export-'+tbl.id;
    var input = document.getElementById(fid); var clearBtn = document.getElementById(cid); var exportBtn=document.getElementById(eid);
    function refresh(){ applyFilters(tbl, parseHashQuery(), input?input.value:''); }
    if(input){ input.addEventListener('input', function(){ refresh(); }); }
    if(clearBtn){ clearBtn.addEventListener('click', function(){ if(input) input.value=''; location.hash=''; refresh(); }); }
    if(exportBtn){ exportBtn.addEventListener('click', function(){
      var rows = $all('tbody tr', tbl).filter(function(tr){ return tr.style.display!== 'none'; });
      var csv = [];
      // header
      csv.push($all('th', tbl).map(function(th){ return '"'+(th.textContent||'').trim().replace(/"/g,'""')+'"'; }).join(','));
      rows.forEach(function(tr){
        var cells = $all('td', tr).map(function(td){ return '"'+(td.textContent||'').trim().replace(/"/g,'""')+'"'; });
        csv.push(cells.join(','));
      });
      var blob = new Blob([csv.join('\n')], {type:'text/csv;charset=utf-8;'});
      var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = tbl.id + '.csv'; a.click();
      setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
    }); }
    // Initial
    refresh();
  }
  function highlightAnchor(){
    var h = location.hash||''; var id = null;
    if(h.startsWith('#row-')) id = h.slice(1);
    else if(h.includes('#row-')) id = h.split('#').find(function(x){return x.startsWith('row-');});
    if(!id) return;
    var el = document.getElementById(id); if(!el) return;
    el.classList.add('row-highlight');
    el.scrollIntoView({behavior:'smooth', block:'center'});
    setTimeout(function(){ el.classList.remove('row-highlight'); }, 5000);
  }
  function init(){
    $all('table[data-table]').forEach(attachTable);
    // Apply filters on hash change
    window.addEventListener('hashchange', function(){ $all('table[data-table]').forEach(function(tbl){ var fid='filter-'+tbl.id; var input=document.getElementById(fid); applyFilters(tbl, parseHashQuery(), input?input.value:''); }); highlightAnchor(); });
    highlightAnchor();
    // If hash contains query at load, apply
    $all('table[data-table]').forEach(function(tbl){ var fid='filter-'+tbl.id; var input=document.getElementById(fid); applyFilters(tbl, parseHashQuery(), input?input.value:''); });
  }
  if(document.readyState!=='loading') init(); else document.addEventListener('DOMContentLoaded', init);
})();
