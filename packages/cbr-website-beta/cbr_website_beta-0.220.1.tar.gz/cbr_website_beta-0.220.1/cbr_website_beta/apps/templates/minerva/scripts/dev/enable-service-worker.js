function getCurrentTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    return `${hours}:${minutes}:${seconds}`;
}


$('h1').html(`Enabling Service workers (@ ${getCurrentTime()})`);

// Check if Service Workers are supported

navigator.serviceWorker.register('/service-worker.js', { scope: '/' })
    .then(function(registration) {
            console.log('Service Worker registered with scope:', registration.scope);
        }, function(err) {
            // Registration failed :(
            console.log('Service Worker registration failed:', err);
        });

// navigator.serviceWorker.getRegistrations().then(function(registrations) {
//   for(let registration of registrations) {
//     registration.unregister();
//     console.log('Unregistered service worker')
//   }
// });