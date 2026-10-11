// Access gate for the whole site (Vercel Routing Middleware, Edge runtime).
//
// The access code is NOT in this repository. It is read from the Vercel
// environment variable ACCESS_CODE. Without that variable the site stays closed.
//
// Flow: a visitor without a valid cookie gets the code form. A correct code sets
// an HttpOnly cookie holding an HMAC derived from the code, valid for 30 days.
// Changing ACCESS_CODE in Vercel invalidates every existing cookie.

export const config = { matcher: '/:path*' };

const COOKIE = 'eko_access';
const MAX_AGE = 60 * 60 * 24 * 30;
const LOGIN_PATH = '/__access';

async function tokenFor(code) {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey('raw', enc.encode(code), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, enc.encode('eko-matrice-follow:v1'));
  return Array.from(new Uint8Array(sig)).map((b) => b.toString(16).padStart(2, '0')).join('');
}

// Compare two strings without stopping at the first difference.
function sameString(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function readCookie(request, name) {
  const header = request.headers.get('cookie') || '';
  for (const part of header.split(';')) {
    const i = part.indexOf('=');
    if (i > -1 && part.slice(0, i).trim() === name) return part.slice(i + 1).trim();
  }
  return '';
}

// Only same-site relative paths are accepted as a return target.
function safeTarget(value) {
  return typeof value === 'string' && /^\/(?!\/)[\w\-./~%#?=&]*$/.test(value) ? value : '/';
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function page(body, status) {
  return new Response(
    `<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>EKO · Accès équipe</title>
<style>
  :root { --eko: #1E64C8; --bg: #f4f7fb; --card: #fff; --text: #16202e; --mute: #6b7889; --line: #b4c0d0; --err: #a32d2d; }
  @media (prefers-color-scheme: dark) { :root { --bg: #0f1621; --card: #17202e; --text: #e8edf4; --mute: #8d9aac; --line: #3d4c62; --err: #f09595; } }
  * { box-sizing: border-box; }
  body { margin: 0; min-height: 100vh; display: grid; place-items: center; padding: 24px 16px;
         background: var(--bg); color: var(--text); font: 16px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
  main { width: 100%; max-width: 380px; padding: 28px; background: var(--card); border: 1px solid var(--line); border-radius: 10px; }
  .eko { font-weight: 700; font-size: 28px; letter-spacing: .04em; color: var(--eko); }
  h1 { margin: 6px 0 4px; font-size: 19px; }
  p { margin: 0 0 16px; color: var(--mute); font-size: 14.5px; }
  label { display: block; margin-bottom: 6px; font-size: 14px; font-weight: 600; }
  input { width: 100%; height: 44px; padding: 0 12px; font: inherit; color: var(--text); background: var(--bg); border: 1px solid var(--line); border-radius: 6px; }
  button { width: 100%; height: 44px; margin-top: 12px; font: inherit; font-weight: 600; color: #fff; background: var(--eko); border: 0; border-radius: 6px; cursor: pointer; }
  input:focus-visible, button:focus-visible { outline: 2px solid var(--eko); outline-offset: 2px; }
  .err { margin: 12px 0 0; color: var(--err); font-size: 14px; }
</style>
</head>
<body>
<main>
  <div class="eko">EKO</div>
  ${body}
</main>
</body>
</html>`,
    { status, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', 'x-robots-tag': 'noindex, nofollow' } }
  );
}

function form(target, error) {
  return page(
    `<h1>Dossier R&amp;D · Accès équipe</h1>
  <p>Document interne Kreativ Labs. Team access only.</p>
  <form method="post" action="${LOGIN_PATH}">
    <input type="hidden" name="to" value="${escapeHtml(target)}">
    <label for="code">Code d'accès</label>
    <input id="code" name="code" type="password" autocomplete="current-password" autofocus required>
    <button type="submit">Entrer</button>
    ${error ? '<p class="err" role="alert">Code incorrect. Vérifiez la saisie et réessayez.</p>' : ''}
  </form>`,
    error ? 401 : 200
  );
}

function next() {
  // Let the request through to the static files.
  return new Response(null, { headers: { 'x-middleware-next': '1' } });
}

export default async function middleware(request) {
  // robots.txt stays readable so crawlers see the "Disallow: /" rule. It holds nothing else.
  if (new URL(request.url).pathname === '/robots.txt') return next();

  const code = (typeof process !== 'undefined' && process.env && process.env.ACCESS_CODE) || '';
  if (!code) {
    return page(`<h1>Accès non configuré</h1><p>Le code d'accès de ce site n'est pas encore défini. Le site reste fermé.</p>`, 503);
  }

  const url = new URL(request.url);
  const expected = await tokenFor(code);

  if (url.pathname === LOGIN_PATH) {
    if (request.method !== 'POST') return Response.redirect(new URL('/', url), 303);
    const data = await request.formData();
    const target = safeTarget(data.get('to'));
    if (!sameString(String(data.get('code') || ''), code)) return form(target, true);
    return new Response(null, {
      status: 303,
      headers: {
        location: target,
        'set-cookie': `${COOKIE}=${expected}; Path=/; Max-Age=${MAX_AGE}; HttpOnly; Secure; SameSite=Lax`,
        'cache-control': 'no-store',
      },
    });
  }

  if (sameString(readCookie(request, COOKIE), expected)) return next();
  return form(safeTarget(url.pathname + url.search), false);
}
