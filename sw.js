/**
 * Dufengxun.com - Service Worker
 * Provides offline caching for the marketing site
 */

const CACHE_NAME = 'dufengxun-v1';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/services.html',
    '/culture.html',
    '/updates.html',
    '/insights.html',
    '/contact.html',
    '/privacy.html',
    '/terms.html',
    '/404.html',
    '/css/style.css',
    '/js/components.js',
    '/js/main.js',
    '/js/app.js',
    '/images/favicon.svg',
    '/images/logo.svg',
    '/images/og-default.png',
    '/images/hero-illustration.png',
    '/images/pattern.png',
    '/manifest.json'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_ASSETS).catch((err) => {
                console.warn('Cache addAll partial failure:', err);
            });
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;
    if (!event.request.url.startsWith(self.location.origin)) return;

    event.respondWith(
        caches.match(event.request).then((cached) => {
            if (cached) return cached;

            return fetch(event.request).then((response) => {
                if (!response || response.status !== 200 || response.type !== 'basic') {
                    return response;
                }
                const toCache = response.clone();
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(event.request, toCache);
                });
                return response;
            }).catch(() => {
                if (event.request.mode === 'navigate') {
                    return caches.match('/404.html') || caches.match('/index.html');
                }
            });
        })
    );
});
