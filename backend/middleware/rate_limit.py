"""
Rate Limiting Middleware
Implements token bucket algorithm for API rate limiting
"""

import time
from collections import defaultdict
from typing import Callable, Dict, Tuple

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class TokenBucket:
    """Token bucket for rate limiting."""

    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket.

        Args:
            capacity: Maximum number of tokens
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens from bucket.

        Args:
            tokens: Number of tokens to consume

        Returns:
            bool: True if tokens consumed, False if insufficient
        """
        self._refill()

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill

        # Add tokens based on elapsed time
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

    def remaining(self) -> int:
        """Get remaining tokens."""
        self._refill()
        return int(self.tokens)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using token bucket algorithm.

    Default limits:
    - 100 requests per minute per IP
    - Burst capacity of 20 requests
    """

    def __init__(
        self,
        app: ASGIApp,
        requests_per_minute: int = 100,
        burst_size: int = 20,
    ):
        """
        Initialize rate limiter.

        Args:
            app: ASGI application
            requests_per_minute: Sustained request rate limit
            burst_size: Burst capacity
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.burst_size = burst_size
        self.buckets: Dict[str, TokenBucket] = defaultdict(
            lambda: TokenBucket(
                capacity=burst_size,
                refill_rate=requests_per_minute / 60.0,
            )
        )

    def _get_client_identifier(self, request: Request) -> str:
        """
        Get unique client identifier.

        Args:
            request: Incoming request

        Returns:
            str: Client identifier (IP address or API key)
        """
        # Check for X-Forwarded-For (behind proxy)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

        # Check for X-Real-IP
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fall back to direct client IP
        if request.client:
            return request.client.host

        return "unknown"

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request with rate limiting.

        Args:
            request: Incoming request
            call_next: Next middleware in chain

        Returns:
            Response or rate limit error
        """
        # Skip rate limiting for health checks
        if request.url.path in ["/api/v1/healthz", "/api/v1/livez", "/api/v1/readyz"]:
            return await call_next(request)

        client_id = self._get_client_identifier(request)
        bucket = self.buckets[client_id]

        # Try to consume a token
        if not bucket.consume():
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate Limit Exceeded",
                    "message": f"Maximum {self.requests_per_minute} requests per minute allowed",
                    "retry_after": 60,
                },
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": "60",
                },
            )

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(bucket.remaining())

        return response
