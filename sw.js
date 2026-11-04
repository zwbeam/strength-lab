const CACHE='strength-lab-v28';
const ASSETS=['./index.html','./styles.css','./app.js','./manifest.webmanifest','./icon-192.png','./icon-512.png','./header-strengthlab-v23.webp','./header-traininghub-v23.webp','./header-traininglog-v23.webp','./header-settings-v23.webp','./background-v23.webp','./background-workout-v28.webp','./header-workout-v28.webp'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(ASSETS)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('strength-lab-')&&key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',event=>{
 const request=event.request;
 if(request.method!=='GET'||new URL(request.url).origin!==self.location.origin)return;
 event.respondWith(fetch(request,{cache:'no-store'}).then(response=>{
  if(response.ok){const copy=response.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put(request,copy)))}
  return response;
 }).catch(async()=> (await caches.match(request)) || (request.mode==='navigate' ? await caches.match('./index.html'):Response.error())));
});
