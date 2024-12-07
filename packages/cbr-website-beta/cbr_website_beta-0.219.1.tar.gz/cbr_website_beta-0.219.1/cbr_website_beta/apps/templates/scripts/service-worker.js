const version = '{{version}}';
const CACHE_NAME = 'site-cache-' + version;

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request, {cacheName: CACHE_NAME})
            .then(function(response) {  // Cache hit - return the response from the cached version
                if (response) {
                    console.log(`[${version}][SW:fetch][cache-hit] `, event.request.url);
                    return response;
                }
                return fetch(event.request);    // Not in cache - return the result from the network
            })
    );
});

self.addEventListener('install', event => {
    console.log('[SERVICE WORKER] Installing');
    // Force the waiting service worker to become the active service worker
    event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', event => {
    console.log('[SERVICE WORKER] Activating');
    // Take control of all clients as soon as the service worker is active
    event.waitUntil(self.clients.claim());
});

console.log('[SERVICE WORKER] All setup');
