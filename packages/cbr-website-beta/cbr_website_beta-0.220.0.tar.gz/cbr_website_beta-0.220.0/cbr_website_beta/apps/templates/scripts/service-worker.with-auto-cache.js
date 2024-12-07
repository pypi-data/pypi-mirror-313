let version = '{{version}}'
const CACHE_NAME = 'site-cache-' + version;

function on_service_worker_fetch(event) {

    if (event.request.url.includes('google-analytics.com') || event.request.url.includes('googletagmanager.com')) {
        console.log(`[${version}][SW:fetch] Blocked GA request: `, 'google-analytics.com');
        // Respond with an empty 200 OK response to effectively "block" it
        event.respondWith(new Response('', {status: 200, statusText: 'Blocked GA'}));
        return;
    }

    // Only handle GET requests in the cache logic
    if (event.request.method !== 'GET') {
        console.log(`[${version}][SW:fetch] Non-GET request not cached: `, event.request.url);
        event.respondWith(fetch(event.request));
        return;
    }



    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                // Cache hit - return the response from the cached version
                if (response) {
                    //console.log(`[${version}][SW:fetch][cache-hit] `, event.request.url);
                    return response;
                }

                // Not in cache - return the result from the network and cache it
                return fetch(event.request).then(function(response) {
                    // Check if we received a valid response
                    console.log(`[${version}][SW:fetch][request] `, event.request.url);
                    if (!response || response.status !== 200 || (response.type !== 'basic' && response.type !== 'cors') ) {
                        if (response.status !==0 && response.type !== 'opaque') {
                            console.log(response.type, response.status)
                            return response;
                        }
                    }
                    console.log(`[${version}][SW:fetch][saving] `, event.request.url);
                    var responseToCache = response.clone();

                    caches.open(CACHE_NAME)
                        .then(function(cache) {
                            cache.put(event.request, responseToCache);
                        });

                    return response;
                });
            })
    );
}

// Listen for the 'fetch' event on the Service Worker
self.addEventListener('fetch', function(event) {
    //event.respondWith(fetch(event.request));
    on_service_worker_fetch(event)
});

self.addEventListener('install', event => {
  event.waitUntil(self.skipWaiting()); // Activates the new SW immediately
});

// Take control of the page as soon as it's active
self.addEventListener('activate', event => {
    event.waitUntil(self.clients.claim()); // Service Worker takes control of all clients immediately
});

console.log('[SERVICE WORKER] all setup')



    // Log the URL of the request to the console
    // let path_to_match = '/b'
    // const requestUrl = new URL(event.request.url);
    //
    // if (requestUrl.pathname === path_to_match) {
    //     console.log('[SW:fetch] ', event.request.url);
    //     // Create a custom response directly in the Service Worker
    //     event.respondWith(new Response('BBBBB This is the custom content for the URL.', {
    //         headers: { 'Content-Type': 'text/plain' } // Set the content type appropriately
    //     }));
    // } else {
        // Perform the fetch as usual for all other requests