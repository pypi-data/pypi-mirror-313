// Open the specific cache
version = 'v0.76.37'
text = `Changed by Minerva! ${version}`

caches.open(`site-cache-${version}`).then(cache => {
    // Create a new response
    const newContent = `<h1>${text}</h1>`;
    const newResponse = new Response(newContent, {
        headers: {'Content-Type': 'text/html'}
    });

    // Update the cache with the new response for a specific URL
    cache.put('/user/chat-threads', newResponse).then(() => {
        console.log('Cache entry updated with new HTML content.');
    }).catch(error => {
        console.error('Error updating the cache:', error);
    });
});
