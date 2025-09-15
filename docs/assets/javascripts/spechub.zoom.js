/* Spechub zoom helpers: expose reset/initialize and bind to coverage/userflow if needed */
(function(){
  'use strict';
  function ready(fn){ if(document.readyState!=='loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }
  ready(function(){
    if (window.spechubInitZoom) {
      window.spechubInitZoom('userflow-object');
      window.spechubInitZoom('coverage-object');
    }
  });
})();
