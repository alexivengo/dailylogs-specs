(function(){
  'use strict';
  // Copy current page URL to clipboard
  window.spechubCopyLink = function(){
    try {
      const url = window.location.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function(){
          announce('Link copied');
        }).catch(function(){
          fallback(url);
        });
      } else {
        fallback(url);
      }
    } catch(e) { /* noop */ }
  };
  function fallback(text){
    const ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly','');
    ta.style.position='absolute'; ta.style.left='-9999px';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); announce('Link copied'); } catch(e) {}
    document.body.removeChild(ta);
  }
  function announce(msg){
    try {
      let live = document.getElementById('spechub-live');
      if(!live){
        live = document.createElement('div');
        live.id='spechub-live'; live.setAttribute('aria-live','polite');
        live.style.position='absolute'; live.style.left='-9999px';
        document.body.appendChild(live);
      }
      live.textContent = msg;
    } catch(e) {}
  }

  // Basic pan/zoom for embedded SVG via <object>
  // Exposed as window.spechubInitZoom and window.spechubResetView
  const zoomStates = new Map();
  function initPanZoomForObject(objId){
    var obj = document.getElementById(objId);
    if(!obj) return;
    if(obj.tagName.toLowerCase() !== 'object') return;
    var setup = function(){
      try{
        var doc = obj.contentDocument; if(!doc) return;
        var svg = doc.querySelector('svg'); if(!svg) return;
        // Ensure viewBox
        if(!svg.hasAttribute('viewBox')){
          var w = parseFloat(svg.getAttribute('width'))||1000;
          var h = parseFloat(svg.getAttribute('height'))||600;
          svg.setAttribute('viewBox', '0 0 '+w+' '+h);
        }
        svg.setAttribute('preserveAspectRatio','xMidYMid meet');
        var vb = svg.getAttribute('viewBox').split(/\s+/).map(parseFloat);
        var initVB = vb.slice();
        var state = { dragging:false, lastX:0, lastY:0, minScale:0.3, maxScale:8, pinchDist:null };
        zoomStates.set(objId, { svg: svg, get vb(){return vb;}, setVB: setViewBox, initVB: initVB });
        function setViewBox(x,y,w,h){ svg.setAttribute('viewBox', [x,y,w,h].join(' ')); vb=[x,y,w,h]; }
        function onWheel(e){
          e.preventDefault();
          var delta = e.deltaY < 0 ? -1 : 1;
          // Ctrl+wheel -> stronger zoom
          var scaleBase = e.ctrlKey ? 1.25 : 1.1;
          var scale = (delta>0) ? scaleBase : (1/scaleBase);
          var newW = Math.max(10, Math.min(vb[2]*scale, vb[2]/state.minScale*state.maxScale));
          // Keep center on cursor
          var pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
          var ctm = svg.getScreenCTM().inverse();
          var loc = pt.matrixTransform(ctm);
          var k = newW / vb[2];
          var newH = vb[3]*k;
          var nx = loc.x - (loc.x - vb[0]) * k;
          var ny = loc.y - (loc.y - vb[1]) * k;
          setViewBox(nx, ny, newW, newH);
        }
        function onDown(e){ state.dragging=true; state.lastX=e.clientX; state.lastY=e.clientY; e.preventDefault(); }
        function onMove(e){ if(!state.dragging) return; var dx=e.clientX-state.lastX; var dy=e.clientY-state.lastY; state.lastX=e.clientX; state.lastY=e.clientY; setViewBox(vb[0]-dx, vb[1]-dy, vb[2], vb[3]); e.preventDefault(); }
        function onUp(){ state.dragging=false; }
        // Basic pinch-zoom
        function dist(t1, t2){ var dx=t2.clientX-t1.clientX, dy=t2.clientY-t1.clientY; return Math.hypot(dx,dy); }
        function onTouchStart(e){ if(e.touches.length===2){ state.pinchDist=dist(e.touches[0], e.touches[1]); e.preventDefault(); } }
        function onTouchMove(e){ if(e.touches.length===2 && state.pinchDist){ e.preventDefault(); var d=dist(e.touches[0], e.touches[1]); var scale = d/state.pinchDist; var newW = Math.max(10, Math.min(vb[2]/scale, vb[2]/state.minScale*state.maxScale)); var k = newW / vb[2]; var newH = vb[3]*k; setViewBox(vb[0], vb[1], newW, newH); state.pinchDist=d; } }
        function onTouchEnd(){ state.pinchDist=null; }
        svg.addEventListener('wheel', onWheel, {passive:false});
        svg.addEventListener('mousedown', onDown);
        svg.addEventListener('mousemove', onMove);
        svg.addEventListener('mouseup', onUp);
        svg.addEventListener('mouseleave', onUp);
        svg.addEventListener('touchstart', onTouchStart, {passive:false});
        svg.addEventListener('touchmove', onTouchMove, {passive:false});
        svg.addEventListener('touchend', onTouchEnd);
        svg.addEventListener('touchcancel', onTouchEnd);
      }catch(e){}
    };
    if(obj.contentDocument && obj.contentDocument.readyState === 'complete') setup();
    else obj.addEventListener('load', setup, { once:true });
  }
  function resetView(objId){
    try{
      var s = zoomStates.get(objId); if(!s) return; var vb = s.initVB; s.setVB(vb[0],vb[1],vb[2],vb[3]);
    }catch(e){}
  }
  window.spechubInitZoom = initPanZoomForObject;
  window.spechubResetView = resetView;

  document.addEventListener('DOMContentLoaded', function(){
    initPanZoomForObject('userflow-object');
    initPanZoomForObject('coverage-object');
  });
})();
