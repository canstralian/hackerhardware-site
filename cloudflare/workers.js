/**
 * Cloudflare Worker for HackerHardware.net
 * Handles routing, DDoS protection, and request filtering
 */

const API_ENDPOINT = 'https://api.hackerhardware.net';
const RATE_LIMIT = 100; // requests per minute
const BLOCKED_COUNTRIES = []; // Add country codes to block if needed

// Rate limiting using Cloudflare KV
async function checkRateLimit(ip) {
  if (typeof RATE_LIMIT_KV === "undefined") {
    // KV binding is missing; disable rate limiting gracefully
    // Optionally, log a warning if logging is available
    return true;
  }
  const key = `rate_limit:${ip}`;
  const count = await RATE_LIMIT_KV.get(key);
  
  if (count && parseInt(count) > RATE_LIMIT) {
    return false;
  }
  
  const newCount = count ? parseInt(count) + 1 : 1;
  await RATE_LIMIT_KV.put(key, newCount.toString(), { expirationTtl: 60 });
  
  return true;
}

async function handleRequest(request) {
  const url = new URL(request.url);
  const ip = request.headers.get('CF-Connecting-IP');
  const country = request.headers.get('CF-IPCountry');
  
  // Block requests from specific countries if configured
  if (BLOCKED_COUNTRIES.includes(country)) {
    return new Response('Access denied', { status: 403 });
  }
  
  // Rate limiting
  const withinLimit = await checkRateLimit(ip);
  if (!withinLimit) {
    return new Response('Rate limit exceeded', { 
      status: 429,
      headers: {
        'Retry-After': '60'
      }
    });
  }
  
  // Security headers
  const securityHeaders = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'",
    'Referrer-Policy': 'strict-origin-when-cross-origin'
  };
  
  // Route to API
  if (url.pathname.startsWith('/api/')) {
    const apiUrl = `${API_ENDPOINT}${url.pathname}${url.search}`;
    const apiRequest = new Request(apiUrl, request);
    
    const response = await fetch(apiRequest);
    const newResponse = new Response(response.body, response);
    
    // Add security headers
    Object.entries(securityHeaders).forEach(([key, value]) => {
      newResponse.headers.set(key, value);
    });
    
    return newResponse;
  }
  
  // Serve static content or redirect to frontend
  return new Response('HackerHardware.net - Living Edge Intelligence', {
    headers: {
      'Content-Type': 'text/html',
      ...securityHeaders
    }
  });
}

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});
