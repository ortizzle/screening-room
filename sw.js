/* Screening Room service worker — network-first app shell */
var CACHE = 'sr-shell-v25'; // v3.4 · Drive Copy

self.addEventListener('install', function(e){
  e.waitUntil(caches.open(CACHE).then(function(c){ return c.addAll(['./', './index.html', './ortiz-drive.js']); }));
  self.skipWaiting();
});

self.addEventListener('activate', function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.filter(function(k){ return k !== CACHE; }).map(function(k){ return caches.delete(k); }));
  }));
  self.clients.claim();
});

self.addEventListener('fetch', function(e){
  // Navigations to the app shell (and ortiz-drive.js below); TMDB/API traffic passes through untouched.
  if(e.request.mode === 'navigate'){
    e.respondWith(
      fetch(e.request).then(function(res){
        var copy = res.clone();
        caches.open(CACHE).then(function(c){ c.put('./index.html', copy); });
        return res;
      }).catch(function(){
        return caches.match('./index.html');
      })
    );
    return;
  }
  // The Drive helper is the shell's one other local script: network-first too,
  // with the cached copy so the app still opens offline.
  var url = new URL(e.request.url);
  if(url.origin === self.location.origin && url.pathname.slice(-15) === '/ortiz-drive.js'){
    e.respondWith(
      fetch(e.request).then(function(res){
        if(res.ok){ var copy = res.clone(); caches.open(CACHE).then(function(c){ c.put('./ortiz-drive.js', copy); }); }
        return res;
      }).catch(function(){
        return caches.match('./ortiz-drive.js');
      })
    );
  }
});
