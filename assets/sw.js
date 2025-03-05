const CACHE_VERSION = 'V0.0.3';
const CACHE_NAME = `to-do-easy-cache-${CACHE_VERSION}`;

// URLs normalizadas sin barras diagonales finales
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
  self.skipWaiting(); // Forzar activación inmediata
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
  self.clients.claim(); // Tomar control de todas las pestañas
});

self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);
  const pathname = requestUrl.pathname;

  // Ignorar solicitudes no GET y extensiones
  if (event.request.method !== 'GET' || requestUrl.protocol.startsWith('chrome-extension')) {
    event.respondWith(fetch(event.request).catch(() => {}));
    return;
  }

  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      if (cachedResponse) return cachedResponse;

      // Manejo especial para navegación (documentos HTML)
      if (event.request.destination === 'document') {
        const altPath = pathname.endsWith('/') 
          ? pathname.slice(0, -1) 
          : pathname + '/';
        
        return caches.match(altPath)
          .then(altResponse => altResponse || caches.match('/'))
          .catch(() => caches.match('/'));
      }

      // Intentar red y cachear dinámicamente
      return fetch(event.request)
        .then(response => {
          if (!response || response.status !== 200) return response;

          const responseToCache = response.clone();
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache);
              console.log('Cacheado dinámicamente:', event.request.url);
            });
          return response;
        })
        .catch(() => {
          console.log('Offline, buscando alternativas:', event.request.url);
          return caches.match(event.request)
            || (event.request.destination === 'document' && caches.match('/'))
            || new Response('Offline: Recurso no disponible', { status: 503 });
        });
    })
  );
});