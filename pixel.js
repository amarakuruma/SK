// ====== PIXEL META (Facebook / Instagram) ======
// Coller ici le numéro du pixel (Gestionnaire d'événements → Sources de données), ex. '1234567890123456'
const PIXEL_ID = '';
// ===============================================
// Mesure : visite de la page (PageView), fiche d'une pièce vue (ViewContent),
// clic vers WhatsApp (Contact). Rien n'est envoyé tant que PIXEL_ID est vide.
(function () {
  if (!PIXEL_ID) return;
  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', PIXEL_ID);
  fbq('track', 'PageView');
  const m = location.pathname.match(/^\/p\/(\d+)\/?$/);
  if (m) fbq('track', 'ViewContent', { content_ids: ['N' + m[1]], content_type: 'product', currency: 'GNF' });
  document.addEventListener('click', e => {
    const a = e.target.closest && e.target.closest('a[href*="wa.me"]');
    if (!a) return;
    const n = (decodeURIComponent(a.href).match(/N° (\d+)/) || [])[1];
    fbq('track', 'Contact', n ? { content_ids: ['N' + n] } : {});
  }, true);
})();
