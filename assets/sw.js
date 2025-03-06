const CACHE_VERSION = 'V0.0.4';
const CACHE_NAME = `to-do-easy-cache-${CACHE_VERSION}`;

const urlsToCache = [
  '/',
  '/drops-6392473_640.jpg',
  '/manifest.json',
  '/icon-192x192.png',
  '/icon-512x512.png',
  '/logo.jpg',
  '/nophoto.jpg',
  '/favicon.ico',
  '/marykay_index',
  '/amazon_index',
  '/tasks'
];

self.addEventListener('install', (event) => {
  console.log('Service Worker: Instalando versión', CACHE_VERSION);
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cacheando recursos esenciales');
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.error('Error en precacheo:', error);
      })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activado');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Eliminando caché antiguo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);
  const pathname = requestUrl.pathname;

  if (event.request.method !== 'GET' || requestUrl.protocol.startsWith('chrome-extension')) {
    event.respondWith(fetch(event.request).catch(() => {}));
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        if (cachedResponse) {
          console.log('Sirviendo desde caché:', requestUrl);
          return cachedResponse;
        }

        // Intentar la red primero para rutas dinámicas
        return fetch(event.request)
          .then(networkResponse => {
            if (!networkResponse || networkResponse.status !== 200) {
              console.log('Respuesta de red inválida:', networkResponse.status);
              return networkResponse;
            }
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME)
              .then(cache => {
                console.log('Cacheado dinámicamente:', requestUrl);
                cache.put(event.request, responseToCache);
              })
              .catch(error => {
                console.error('Error al cachear dinámicamente:', error);
              });
            return networkResponse;
          })
          .catch(() => {
            console.log('Sin red, manejando offline:', requestUrl);
            if (event.request.destination === 'document') {
              const altPath = pathname.endsWith('/') ? pathname.slice(0, -1) : pathname + '/';
              return caches.match(altPath)
                .then(altResponse => {
                  if (altResponse) {
                    console.log('Sirviendo alternativa desde caché:', altPath);
                    return altResponse;
                  }
                  console.log('Usando fallback a /');
                  return caches.match('/') || new Response('Offline, página no disponible', { status: 503 });
                });
            }
            return caches.match(event.request)
              .then(fallbackResponse => {
                if (fallbackResponse) {
                  console.log('Devolviendo recurso cacheado:', requestUrl);
                  return fallbackResponse;
                }
                console.log('Recurso no cacheado y sin red:', requestUrl);
                return new Response('Offline, recurso no disponible', { status: 503 });
              });
          });
      })
  );
});