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
})();
