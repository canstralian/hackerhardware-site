/**
 * Edge Caching Utilities
 * Intelligent caching strategies for edge workers
 */

/**
 * Cache manager with TTL and invalidation support
 */
export class EdgeCache {
  constructor(cacheName = 'default', defaultTTL = 300) {
    this.cacheName = cacheName;
    this.defaultTTL = defaultTTL;
    this.cache = caches.default;
  }

  /**
   * Get from cache or fetch from origin
   */
  async getOrSet(request, fetcher, options = {}) {
    const ttl = options.ttl || this.defaultTTL;
    const cacheKey = this._getCacheKey(request, options.key);

    // Try to get from cache
    let response = await this.cache.match(cacheKey);

    if (response) {
      // Check if stale
      const age = this._getAge(response);
      if (age < ttl) {
        return this._addCacheHeaders(response, 'HIT', age);
      }
    }

    // Cache miss or stale - fetch new data
    response = await fetcher();

    if (response && response.ok) {
      // Add cache control headers
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', `public, max-age=${ttl}`);
      headers.set('X-Cache-Time', new Date().toISOString());

      const cachedResponse = new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers,
      });

      // Store in cache
      await this.cache.put(cacheKey, cachedResponse.clone());

      return this._addCacheHeaders(cachedResponse, 'MISS', 0);
    }

    return response;
  }

  /**
   * Invalidate cache entry
   */
  async invalidate(request, key) {
    const cacheKey = this._getCacheKey(request, key);
    return await this.cache.delete(cacheKey);
  }

  /**
   * Invalidate multiple entries by pattern
   */
  async invalidatePattern(pattern) {
    // Note: Not supported in Cloudflare Workers Cache API
    // Implement using KV or Durable Objects for advanced invalidation
    console.warn('Pattern invalidation not supported in Cache API');
  }

  /**
   * Generate cache key
   */
  _getCacheKey(request, customKey) {
    if (customKey) {
      return new Request(`https://cache.internal/${customKey}`);
    }
    return request;
  }

  /**
   * Get cache age in seconds
   */
  _getAge(response) {
    const cacheTime = response.headers.get('X-Cache-Time');
    if (!cacheTime) return Infinity;

    const cached = new Date(cacheTime);
    const now = new Date();
    return Math.floor((now - cached) / 1000);
  }

  /**
   * Add cache status headers
   */
  _addCacheHeaders(response, status, age) {
    const headers = new Headers(response.headers);
    headers.set('X-Cache-Status', status);
    headers.set('X-Cache-Age', age.toString());

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  }
}

/**
 * Conditional caching based on request/response
 */
export function shouldCache(request, response) {
  // Don't cache if not GET/HEAD
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    return false;
  }

  // Don't cache error responses
  if (!response.ok) {
    return false;
  }

  // Don't cache if Cache-Control says not to
  const cacheControl = response.headers.get('Cache-Control');
  if (cacheControl && (
    cacheControl.includes('no-cache') ||
    cacheControl.includes('no-store') ||
    cacheControl.includes('private')
  )) {
    return false;
  }

  return true;
}

/**
 * Get cache TTL from response headers
 */
export function getCacheTTL(response, defaultTTL = 300) {
  const cacheControl = response.headers.get('Cache-Control');

  if (cacheControl) {
    const maxAge = cacheControl.match(/max-age=(\d+)/);
    if (maxAge) {
      return parseInt(maxAge[1], 10);
    }
  }

  return defaultTTL;
}
