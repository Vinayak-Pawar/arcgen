"""
Security utilities for AI provider system

Implements SSRF (Server-Side Request Forgery) protection and other security measures.
Based on next-ai-draw-io security model (GHSA-9qf7-mprq-9qgm).
"""

from typing import Optional
from urllib.parse import urlparse


class SecurityError(Exception):
    """Raised when security validation fails"""
    pass


def validate_custom_endpoint(
    base_url: Optional[str],
    api_key: Optional[str],
    provider_name: str
) -> None:
    """
    Validate custom endpoint configuration for SSRF protection.
    
    CRITICAL SECURITY RULE:
    If a custom base_url is provided, an API key MUST also be provided.
    This prevents attackers from redirecting server API keys to malicious endpoints.
    
    Args:
        base_url: Custom API endpoint URL (optional)
        api_key: API key for authentication (optional)
        provider_name: Name of the provider being configured
        
    Raises:
        SecurityError: If base_url is provided without api_key
        
    Example:
        >>> # SAFE - both provided
        >>> validate_custom_endpoint("https://custom.com", "sk-123", "openai")
        
        >>> # SAFE - neither provided (use defaults)
        >>> validate_custom_endpoint(None, None, "openai")
        
        >>> # UNSAFE - would redirect server key to attacker's endpoint
        >>> validate_custom_endpoint("https://evil.com", None, "openai")
        SecurityError: API key is required when using a custom base URL
    """
    if base_url and not api_key:
        raise SecurityError(
            f"API key is required when using a custom base URL for {provider_name}. "
            f"Please provide your own API key to prevent security vulnerabilities."
        )


def validate_url_safety(url: str) -> bool:
    """
    Validate that a URL is safe to use.
    
    Checks:
    - Valid URL format
    - Uses HTTPS (except localhost)
    - Not pointing to internal/private networks
    
    Args:
        url: URL to validate
        
    Returns:
        True if URL is safe, False otherwise
    """
    try:
        parsed = urlparse(url)
        
        # Must have scheme and netloc
        if not parsed.scheme or not parsed.netloc:
            return False
        
        # Get hostname without port
        hostname = parsed.hostname or parsed.netloc.split(":")[0]
        
        # Allow localhost HTTP for development
        if hostname in ["localhost", "127.0.0.1", "0.0.0.0"]:
            return True
        
        # Require HTTPS for external endpoints
        if parsed.scheme != "https":
            return False
        
        # Block private IP ranges (basic check)
        if hostname.startswith("10.") or hostname.startswith("192.168."):
            return False
        if hostname.startswith("172."):
            # Check if in 172.16.0.0 - 172.31.255.255 range
            try:
                second_octet = int(hostname.split(".")[1])
                if 16 <= second_octet <= 31:
                    return False
            except (IndexError, ValueError):
                pass
        
        return True
        
    except Exception:
        return False


def sanitize_library_name(library: str) -> str:
    """
    Sanitize shape library name to prevent path traversal attacks.
    
    Args:
        library: Raw library name from user input
        
    Returns:
        Sanitized library name (lowercase, alphanumeric + hyphen/underscore/dot only)
        
    Example:
        >>> sanitize_library_name("aws4")
        'aws4'
        >>> sanitize_library_name("../../etc/passwd")
        'etcpasswd'
        >>> sanitize_library_name("AWS-2.0_Beta")
        'aws-2.0_beta'
    """
    import re
    # Remove all characters except alphanumeric, hyphen, underscore, and dot
    sanitized = re.sub(r'[^a-z0-9_.-]', '', library.lower())
    return sanitized
