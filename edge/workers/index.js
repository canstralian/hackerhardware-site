/**
 * HackerHardware.net - Edge Worker
 * Main edge computing router with intelligent traffic management
 */

// Configuration
const CONFIG = {
  BACKEND_URL: 'https://api.hackerhardware.net',
  STATIC_URL: 'https://hackerhardware.net',
  CACHE_TTL: 300, // 5 minutes
  RATE_LIMIT_REQUESTS: 100,
  RATE_LIMIT_WINDOW: 60, // seconds
};

// Security headers
const SECURITY_HEADERS = {
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'X-XSS-Protection': '1; mode=block',
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
};

/**
 * Main request handler
 */
export default {
  async fetch(request, env, ctx) {
    try {
      const url = new URL(request.url);
      const path = url.pathname;

      // Add request ID for tracing
      const requestId = crypto.randomUUID();

      // Route based on path
      if (path === '/healthz' || path === '/edge/healthz') {
        return handleHealthCheck(requestId);
      }

      if (path.startsWith('/api/')) {
        return await handleApiRequest(request, env, requestId);
      }

      if (path.startsWith('/static/') || path.startsWith('/assets/')) {
        return await handleStaticRequest(request, env, requestId);
      }

      // Default: serve static site
      return await handleStaticRequest(request, env, requestId);

    } catch (error) {
      return handleError(error, request);
    }
  },
};

/**
 * Health check endpoint
 */
function handleHealthCheck(requestId) {
  const response = {
    status: 'healthy',
    edge: 'operational',
    timestamp: new Date().toISOString(),
    region: globalThis.CLOUDFLARE_REGION || 'unknown',
    requestId: requestId,
  };

  return new Response(JSON.stringify(response, null, 2), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'X-Request-ID': requestId,
      ...SECURITY_HEADERS,
    },
  });
}

/**
 * API request handler with backend proxying
 */
async function handleApiRequest(request, env, requestId) {
  const url = new URL(request.url);

  // Construct backend URL
  const backendUrl = `${CONFIG.BACKEND_URL}${url.pathname}${url.search}`;

  // Create new request with additional headers
  const backendRequest = new Request(backendUrl, {
    method: request.method,
    headers: request.headers,
    body: request.body,
  });

  // Add edge metadata headers
  backendRequest.headers.set('X-Edge-Region', globalThis.CLOUDFLARE_REGION || 'unknown');
  backendRequest.headers.set('X-Request-ID', requestId);

  try {
    // Fetch from backend with timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout

    const response = await fetch(backendRequest, {
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    // Add security headers to response
    const headers = new Headers(response.headers);
    Object.entries(SECURITY_HEADERS).forEach(([key, value]) => {
      headers.set(key, value);
    });
    headers.set('X-Request-ID', requestId);
    headers.set('X-Edge-Cache', 'MISS');

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: headers,
    });

  } catch (error) {
    // Backend timeout or error
    return new Response(JSON.stringify({
      error: 'Backend Unavailable',
      message: 'The backend service is temporarily unavailable',
      requestId: requestId,
    }), {
      status: 503,
      headers: {
        'Content-Type': 'application/json',
        'X-Request-ID': requestId,
        'Retry-After': '30',
        ...SECURITY_HEADERS,
      },
    });
  }
}

/**
 * Static content handler with edge caching
 */
async function handleStaticRequest(request, env, requestId) {
  const url = new URL(request.url);
  const cache = caches.default;

  // Check cache first
  let response = await cache.match(request);

  if (response) {
    // Cache hit
    const headers = new Headers(response.headers);
    headers.set('X-Edge-Cache', 'HIT');
    headers.set('X-Request-ID', requestId);

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: headers,
    });
  }

  // Cache miss - fetch from origin
  const staticUrl = `${CONFIG.STATIC_URL}${url.pathname}${url.search}`;

  try {
    response = await fetch(staticUrl, {
      cf: {
        cacheTtl: CONFIG.CACHE_TTL,
        cacheEverything: true,
      },
    });

    // Clone response to cache it
    const responseToCache = response.clone();

    // Add headers
    const headers = new Headers(response.headers);
    headers.set('X-Edge-Cache', 'MISS');
    headers.set('X-Request-ID', requestId);
    headers.set('Cache-Control', `public, max-age=${CONFIG.CACHE_TTL}`);
    Object.entries(SECURITY_HEADERS).forEach(([key, value]) => {
      headers.set(key, value);
    });

    const finalResponse = new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: headers,
    });

    // Cache for future requests
    ctx.waitUntil(cache.put(request, responseToCache));

    return finalResponse;

  } catch (error) {
    return handleError(error, request, requestId);
  }
}

/**
 * Error handler
 */
function handleError(error, request, requestId = 'unknown') {
  console.error('Edge Worker Error:', error);

  const errorResponse = {
    error: 'Internal Server Error',
    message: 'An unexpected error occurred at the edge',
    requestId: requestId,
    path: new URL(request.url).pathname,
  };

  return new Response(JSON.stringify(errorResponse, null, 2), {
    status: 500,
    headers: {
      'Content-Type': 'application/json',
      'X-Request-ID': requestId,
      ...SECURITY_HEADERS,
    },
  });
}
