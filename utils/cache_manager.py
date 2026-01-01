# coding=utf-8
from typing import Any, Dict


class CacheManager:
    """缓存管理器"""

    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, Any] = {}
        self.max_size = max_size
        self._access_count: Dict[str, int] = {}

    def get(self, key: str) -> Any:
        """获取缓存值"""
        value = self._cache.get(key)
        if value is not None:
            self._access_count[key] = self._access_count.get(key, 0) + 1
        return value

    def set(self, key: str, value: Any):
        """设置缓存值"""
        # 如果缓存已满，删除最不常用的项
        if len(self._cache) >= self.max_size and key not in self._cache:
            # 找到访问次数最少的key
            if self._access_count:
                min_key = min(self._access_count, key=self._access_count.get)
                del self._cache[min_key]
                del self._access_count[min_key]
            else:
                # 如果没有访问记录，删除第一个key
                first_key = next(iter(self._cache))
                del self._cache[first_key]

        self._cache[key] = value
        self._access_count[key] = self._access_count.get(key, 0) + 1

    def clear(self):
        """清空缓存"""
        self._cache.clear()
        self._access_count.clear()
