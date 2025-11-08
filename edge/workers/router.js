/**
 * Advanced Router for Edge Workers
 * Pattern-based routing with middleware support
 */

export class EdgeRouter {
  constructor() {
    this.routes = [];
    this.middleware = [];
  }

  /**
   * Add middleware function
   */
  use(fn) {
    this.middleware.push(fn);
    return this;
  }

  /**
   * Register a route
   */
  route(method, pattern, handler) {
    this.routes.push({
      method: method.toUpperCase(),
      pattern: this._compilePattern(pattern),
      handler,
    });
    return this;
  }

  /**
   * Register GET route
   */
  get(pattern, handler) {
    return this.route('GET', pattern, handler);
  }

  /**
   * Register POST route
   */
  post(pattern, handler) {
    return this.route('POST', pattern, handler);
  }

  /**
   * Register PUT route
   */
  put(pattern, handler) {
    return this.route('PUT', pattern, handler);
  }

  /**
   * Register DELETE route
   */
  delete(pattern, handler) {
    return this.route('DELETE', pattern, handler);
  }

  /**
   * Compile pattern to regex
   */
  _compilePattern(pattern) {
    // Convert /api/:id to regex
    const paramPattern = pattern.replace(/:(\w+)/g, '(?<$1>[^/]+)');
    return new RegExp(`^${paramPattern}$`);
  }

  /**
   * Handle incoming request
   */
  async handle(request, env, ctx) {
    const url = new URL(request.url);
    const method = request.method;

    // Create context object
    const context = {
      request,
      env,
      ctx,
      url,
      params: {},
      headers: new Headers(),
    };

    // Run middleware
    for (const mw of this.middleware) {
      await mw(context);
    }

    // Find matching route
    for (const route of this.routes) {
      if (route.method !== method && route.method !== 'ALL') {
        continue;
      }

      const match = url.pathname.match(route.pattern);
      if (match) {
        // Extract route parameters
        context.params = match.groups || {};

        try {
          return await route.handler(context);
        } catch (error) {
          console.error('Route handler error:', error);
          return new Response('Internal Server Error', { status: 500 });
        }
      }
    }

    // No route matched
    return new Response('Not Found', { status: 404 });
  }
}

/**
 * Example usage:
 *
 * const router = new EdgeRouter();
 *
 * router.use(async (ctx) => {
 *   ctx.headers.set('X-Custom-Header', 'value');
 * });
 *
 * router.get('/api/users/:id', async (ctx) => {
 *   const userId = ctx.params.id;
 *   return new Response(`User ${userId}`);
 * });
 *
 * export default {
 *   fetch: (req, env, ctx) => router.handle(req, env, ctx)
 * };
 */
