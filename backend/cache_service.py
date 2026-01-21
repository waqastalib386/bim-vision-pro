"""
BIM Vision Pro - Caching Service
High-performance caching for IFC files and AI analysis results
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class CacheService:
    """
    In-memory cache service for parsed IFC files and AI analysis results
    Provides significant performance improvements for repeated file uploads
    """

    def __init__(self, ttl_hours: int = 24):
        """
        Initialize cache service

        Args:
            ttl_hours: Time-to-live for cached items in hours (default: 24)
        """
        self.file_cache: Dict[str, Dict[str, Any]] = {}
        self.analysis_cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_hours * 3600

        print(f"[CACHE] Cache service initialized (TTL: {ttl_hours}h)")

    @staticmethod
    def get_file_hash(content: bytes) -> str:
        """
        Generate MD5 hash for file content

        Args:
            content: File content in bytes

        Returns:
            MD5 hash string
        """
        return hashlib.md5(content).hexdigest()

    def cache_file_data(self, file_hash: str, data: Dict[str, Any]) -> None:
        """
        Cache parsed IFC file data

        Args:
            file_hash: MD5 hash of file content
            data: Parsed building data
        """
        self.file_cache[file_hash] = {
            'data': data,
            'timestamp': time.time(),
            'cached_at': datetime.now().isoformat()
        }
        print(f"[CACHE] File data cached: {file_hash[:8]}...")

    def get_cached_file_data(self, file_hash: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached file data if available and not expired

        Args:
            file_hash: MD5 hash of file content

        Returns:
            Cached data or None if not found/expired
        """
        if file_hash not in self.file_cache:
            return None

        cached_item = self.file_cache[file_hash]
        age = time.time() - cached_item['timestamp']

        # Check if cache expired
        if age > self.ttl_seconds:
            print(f"[CACHE] Cache expired for {file_hash[:8]}... (age: {age/3600:.1f}h)")
            del self.file_cache[file_hash]
            return None

        print(f"[CACHE] Cache HIT for file {file_hash[:8]}... (age: {age:.1f}s)")
        return cached_item['data']

    def cache_analysis(self, data_signature: str, analysis: str) -> None:
        """
        Cache AI analysis result

        Args:
            data_signature: Signature/hash of building data
            analysis: AI analysis text
        """
        self.analysis_cache[data_signature] = {
            'analysis': analysis,
            'timestamp': time.time(),
            'cached_at': datetime.now().isoformat()
        }
        print(f"[CACHE] Analysis cached: {data_signature[:8]}...")

    def get_cached_analysis(self, data_signature: str) -> Optional[str]:
        """
        Retrieve cached analysis if available and not expired

        Args:
            data_signature: Signature/hash of building data

        Returns:
            Cached analysis or None if not found/expired
        """
        if data_signature not in self.analysis_cache:
            return None

        cached_item = self.analysis_cache[data_signature]
        age = time.time() - cached_item['timestamp']

        # Check if cache expired
        if age > self.ttl_seconds:
            print(f"[CACHE] Analysis cache expired for {data_signature[:8]}... (age: {age/3600:.1f}h)")
            del self.analysis_cache[data_signature]
            return None

        print(f"[CACHE] Cache HIT for analysis {data_signature[:8]}... (age: {age:.1f}s)")
        return cached_item['analysis']

    @staticmethod
    def get_data_signature(data: Dict[str, Any]) -> str:
        """
        Generate signature for building data (for analysis caching)

        Args:
            data: Building data dictionary

        Returns:
            MD5 hash of data
        """
        # Create deterministic string representation
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(data_str.encode()).hexdigest()

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics

        Returns:
            Dictionary with cache stats
        """
        return {
            'file_cache_size': len(self.file_cache),
            'analysis_cache_size': len(self.analysis_cache),
            'ttl_hours': self.ttl_seconds / 3600
        }

    def clear_cache(self) -> None:
        """Clear all cached data"""
        file_count = len(self.file_cache)
        analysis_count = len(self.analysis_cache)

        self.file_cache.clear()
        self.analysis_cache.clear()

        print(f"[CACHE] Cache cleared: {file_count} files, {analysis_count} analyses")

    def cleanup_expired(self) -> None:
        """Remove expired items from cache"""
        current_time = time.time()

        # Cleanup file cache
        expired_files = [
            key for key, value in self.file_cache.items()
            if current_time - value['timestamp'] > self.ttl_seconds
        ]
        for key in expired_files:
            del self.file_cache[key]

        # Cleanup analysis cache
        expired_analyses = [
            key for key, value in self.analysis_cache.items()
            if current_time - value['timestamp'] > self.ttl_seconds
        ]
        for key in expired_analyses:
            del self.analysis_cache[key]

        if expired_files or expired_analyses:
            print(f"[CACHE] Cleaned up {len(expired_files)} files, {len(expired_analyses)} analyses")


# Global cache instance
cache_service = CacheService(ttl_hours=24)
