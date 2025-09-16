(function(){
  'use strict';
  function $(sel, root){return (root||document).querySelector(sel);} 
  function $all(sel, root){return Array.from((root||document).querySelectorAll(sel));}
  function slug(s){return (s||'').toString().trim().toLowerCase().replace(/[^a-z0-9_\-\/:.]+/g,'-');}
  function storageGet(key){
    try {
      if(window.localStorage){ return window.localStorage.getItem(key); }
    } catch(e){}
    return null;
  }
  function storageSet(key, value){
    try {
      if(!window.localStorage) return;
      if(value===null){ window.localStorage.removeItem(key); }
      else { window.localStorage.setItem(key, value); }
    } catch(e){}
  }
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
  function summarizeFilters(filters){
    var parts = [];
    Object.keys(filters).forEach(function(k){ if(filters[k] && filters[k].length){ parts.push(k+'='+filters[k].join(',')); }});
    return parts.join('; ');
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
    var live = $('#live-'+tbl.id); if(live){
      var summary = summarizeFilters(filters);
      live.textContent = summary ? ('Фильтры: '+summary+' (найдено '+visible+')') : ('Найдено: '+visible);
    }
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
    var live = $('#live-'+tbl.id); if(live && th){ live.textContent = 'Сортировка: '+(th.textContent||'')+' '+(dir==='asc'?'по возрастанию':'по убыванию'); }
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
    var fid = 'filter-'+tbl.id;
    var cid = 'clear-'+tbl.id;
    var eid = 'export-'+tbl.id;
    var jsonId = 'export-json-'+tbl.id;
    var copyId = 'copy-'+tbl.id;
    var input = document.getElementById(fid);
    var clearBtn = document.getElementById(cid);
    var exportBtn = document.getElementById(eid);
    var exportJsonBtn = document.getElementById(jsonId);
    var copyBtn = document.getElementById(copyId);
    function refresh(){ applyFilters(tbl, parseHashQuery(), input ? input.value : ''); }
    if(input){ input.addEventListener('input', function(){ refresh(); }); }
    if(clearBtn){ clearBtn.addEventListener('click', function(){ if(input) input.value=''; location.hash=''; refresh(); }); }
    if(copyBtn){ copyBtn.addEventListener('click', function(){
      try{
        var url = location.origin + location.pathname + location.search + location.hash;
        if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(url); }
        else {
          var ta = document.createElement('textarea');
          ta.value = url; ta.setAttribute('readonly','');
          ta.style.position='absolute'; ta.style.left='-9999px';
          document.body.appendChild(ta); ta.select();
          try{ document.execCommand('copy'); }catch(err){}
          document.body.removeChild(ta);
        }
      }catch(e){}
    }); }
    if(exportBtn){ exportBtn.addEventListener('click', function(){
      var rows = $all('tbody tr', tbl).filter(function(tr){ return tr.style.display!=='none'; });
      var csv = [];
      csv.push($all('th', tbl).map(function(th){ return '"'+(th.textContent||'').trim().replace(/"/g,'""')+'"'; }).join(','));
      rows.forEach(function(tr){
        var cells = $all('td', tr).map(function(td){ return '"'+(td.textContent||'').trim().replace(/"/g,'""')+'"'; });
        csv.push(cells.join(','));
      });
      var blob = new Blob([csv.join('\n')], {type:'text/csv;charset=utf-8;'});
      var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = tbl.id + '.csv'; a.click();
      setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
    }); }
    if(exportJsonBtn){ exportJsonBtn.addEventListener('click', function(){
      var rows = $all('tbody tr', tbl).filter(function(tr){ return tr.style.display!=='none'; });
      var headers = $all('th', tbl).map(function(th){ return (th.textContent||'').trim(); });
      var data = rows.map(function(tr){
        var obj = {};
        headers.forEach(function(label, idx){
          var key = label || ('column_'+idx);
          var cell = tr.cells[idx];
          var value = cell ? (cell.textContent||'').trim() : '';
          obj[key] = value;
        });
        return obj;
      });
      var json = JSON.stringify(data, null, 2);
      var blob = new Blob([json], {type:'application/json;charset=utf-8;'});
      var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = tbl.id + '.json'; a.click();
      setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
    }); }
    var columnWrap = document.querySelector('[data-column-menu="'+tbl.id+'"]');
    if(columnWrap){
      var columnBtn = columnWrap.querySelector('.btn-columns');
      var columnMenu = columnWrap.querySelector('.column-visibility-menu');
      var columnInputs = $all('input[data-col-index]', columnWrap);
      var storageKey = 'spechub:columns:'+tbl.id;
      function updateAria(input, checked){
        var parent = input.parentElement;
        if(parent && parent.classList && parent.classList.contains('column-visibility-option')){
          parent.setAttribute('aria-checked', checked ? 'true' : 'false');
        }
      }
      function setColumnVisibility(idx, show){
        $all('tr', tbl).forEach(function(row){
          if(idx >= 0 && idx < row.cells.length){ row.cells[idx].style.display = show ? '' : 'none'; }
        });
      }
      function collectHidden(){
        var hidden = [];
        columnInputs.forEach(function(input){
          if(input.disabled) return;
          var idx = parseInt(input.getAttribute('data-col-index'), 10);
          if(isNaN(idx)) return;
          if(!input.checked) hidden.push(idx);
        });
        return hidden;
      }
      function applyColumnPrefs(){
        var raw = storageGet(storageKey) || '';
        var hidden = raw ? raw.split(',').map(function(x){ var n=parseInt(x,10); return isNaN(n)?null:n; }).filter(function(x){ return x!==null; }) : [];
        var sanitized = [];
        columnInputs.forEach(function(input){
          var idx = parseInt(input.getAttribute('data-col-index'), 10);
          if(isNaN(idx)) return;
          var locked = input.hasAttribute('data-locked') || input.disabled;
          var visible = locked || hidden.indexOf(idx) === -1;
          input.checked = visible;
          setColumnVisibility(idx, visible);
          updateAria(input, visible);
          if(!locked && !visible){ sanitized.push(idx); }
        });
        storageSet(storageKey, sanitized.length ? sanitized.join(',') : null);
      }
      function persistHidden(){
        var hidden = collectHidden();
        storageSet(storageKey, hidden.length ? hidden.join(',') : null);
      }
      columnInputs.forEach(function(input){
        if(input.disabled) return;
        input.addEventListener('change', function(){
          var idx = parseInt(input.getAttribute('data-col-index'), 10);
          if(isNaN(idx)) return;
          var visible = !!input.checked;
          setColumnVisibility(idx, visible);
          updateAria(input, visible);
          persistHidden();
        });
      });
      function closeMenu(){
        if(!columnMenu) return;
        if(columnMenu.hidden) return;
        columnMenu.hidden = true;
        if(columnBtn) columnBtn.setAttribute('aria-expanded','false');
      }
      function openMenu(){
        if(!columnMenu) return;
        columnMenu.hidden = false;
        if(columnBtn) columnBtn.setAttribute('aria-expanded','true');
        var focusTarget = null;
        for(var i=0;i<columnInputs.length;i++){
          var inp = columnInputs[i];
          if(inp && !inp.disabled){ focusTarget = inp; break; }
        }
        if(focusTarget){
          try{ focusTarget.focus(); }catch(e){}
        }
      }
      if(columnBtn && columnMenu){
        columnBtn.addEventListener('click', function(e){
          e.preventDefault();
          e.stopPropagation();
          if(columnMenu.hidden){ openMenu(); }
          else { closeMenu(); }
        });
        document.addEventListener('click', function(ev){ if(!columnWrap.contains(ev.target)){ closeMenu(); } });
        columnMenu.addEventListener('keydown', function(e){ if(e.key==='Escape'){ e.preventDefault(); closeMenu(); columnBtn.focus(); } });
      }
      applyColumnPrefs();
    }
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
    // '/' focuses the first search input
    document.addEventListener('keydown', function(e){
      if(e.key==='/' && !(e.target && (/input|textarea|select/i).test(e.target.tagName))){
        e.preventDefault();
        var inp = document.querySelector('.table-toolbar input[type="search"]'); if(inp){ inp.focus(); }
      }
    });
  }
  if(document.readyState!=='loading') init(); else document.addEventListener('DOMContentLoaded', init);
})();
