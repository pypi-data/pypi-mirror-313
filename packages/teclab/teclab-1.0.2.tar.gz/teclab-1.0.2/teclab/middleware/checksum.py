from .. import utils

class middleware:
    def apply_send(self, data):
        """给数据添加校验和"""
        checksum = utils.md5(data["data"])
        data["data"]+=checksum.encode()+b';'
        return data

    def apply_recv(self, data):
        """验证数据的校验和"""
        checksum = data["data"][-33:-1]
        data["data"] = data["data"][:-33] 
        if utils.md5(data["data"]).encode() == checksum:
            return data
        else:
            print("Checksum failed!")
            print("Data:", data["data"])