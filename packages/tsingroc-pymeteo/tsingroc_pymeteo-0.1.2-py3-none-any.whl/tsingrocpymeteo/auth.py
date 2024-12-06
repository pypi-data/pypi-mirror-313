from typing import Dict
import datetime
import hmac
import base64

__all__ = ["generate_aksk_authorization"]

def generate_aksk_authorization(ak: str, sk: str, query: Dict[str, str]) -> str:
    """
    生成AKSK认证的Authorization头部

    Args:
    - ak (str): 访问密钥
    - sk (str): 秘密密钥
    - query (Dict[str, str]): 查询参数

    Returns:
    - str: Authorization头部字符串
    """

    query_tuple = sorted(query.items())
    query_str = "&".join([f"{k}={v}" for k, v in query_tuple])
    timestamp = int(datetime.datetime.now().timestamp())
    query_str += f"Timestamp={timestamp}"
    # HMAC-SHA256
    signature = hmac.new(sk.encode(), query_str.encode(), "sha256")
    b = signature.digest()
    # base64
    signature = base64.b64encode(b).decode()
    return f"AccessKey={ak},Signature={signature},Timestamp={timestamp}"