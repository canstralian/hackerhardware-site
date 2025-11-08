"""
Security Headers Middleware
Implements OWASP security headers and Zero Trust principles
"""

from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.

    Implements OWASP recommended security headers:
    - X-Content-Type-Options
    - X-Frame-Options
    - X-XSS-Protection
    - Strict-Transport-Security (HSTS)
    - Content-Security-Policy (CSP)
    - Permissions-Policy
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.security_headers = self._get_security_headers()

    def _get_security_headers(self) -> dict:
        """Define security headers configuration."""
        return {
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            # Prevent clickjacking
            "X-Frame-Options": "DENY",
            # Enable XSS protection
            "X-XSS-Protection": "1; mode=block",
            # Enforce HTTPS (1 year)
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
            # Content Security Policy
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:; "
                "connect-src 'self' https://api.hackerhardware.net; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self';"
            ),
            # Permissions Policy (Feature Policy)
            "Permissions-Policy": (
                "geolocation=(), "
                "microphone=(), "
                "camera=(), "
                "payment=(), "
                "usb=(), "
                "magnetometer=(), "
                "gyroscope=(), "
                "accelerometer=()"
            ),
            # Referrer Policy
            "Referrer-Policy": "strict-origin-when-cross-origin",
            # Remove server header
            "X-Powered-By": "Edge Autonomy",
        }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and add security headers to response.

        Args:
            request: Incoming request
            call_next: Next middleware in chain

        Returns:
            Response with security headers
        """
        response = await call_next(request)

        # Add all security headers
        for header, value in self.security_headers.items():
            response.headers[header] = value

        return response
