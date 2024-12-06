# 初始化adapter

from . import manager
from . import tcp

adapters = {
    "tcp": tcp
}

def parse_address(mode,address):
    """解析地址

    Args:
        mode (str): 模式
        address (str): 地址

    Returns:
        str: 协议
        str: 主机
    """
    if '://' in address:
        protocol,address=address.split('://')
    else:
        protocol='tcp'
    if protocol not in adapters:
        raise ValueError(f"Unsupported protocol: {protocol}")
    if mode=='client':
        return adapters[protocol].client(host=address)
    return adapters[protocol].server(host=address)

__all__=["manager","tcp"]