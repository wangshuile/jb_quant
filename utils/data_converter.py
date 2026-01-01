# coding=utf-8
class DataConverter:
    """数据转换工具类"""

    @staticmethod
    def safe_float(value) -> float:
        """安全转换为float类型"""
        try:
            if hasattr(value, '__getitem__'):
                if 'available' in value:
                    return float(value['available'])
                elif 'price' in value:
                    return float(value['price'])
                elif 'volume' in value:
                    return float(value['volume'])
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def safe_int(value) -> int:
        """安全转换为int类型"""
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def safe_str(value) -> str:
        """安全转换为str类型"""
        try:
            return str(value)
        except (TypeError, ValueError):
            return ""
