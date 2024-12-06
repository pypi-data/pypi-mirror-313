import json
from .. import utils

class middleware:
    def __init__(self):
        pass
    
    def apply_send(self, data):
        t={}
        if "data" not in data: data={"data":data}
        for i in data["data"]:
            key=utils.base64_encode(i)
            if type(data["data"][i]) in [dict, list]:
                try:
                    t[key] = json.dumps(data["data"][i])
                except:
                    t[key] = str(data["data"][i])
            else:
                t[key] = str(data["data"][i])
            t[key] = utils.base64_encode(t[key])
        data["data"]=b""
        for i in t.keys():
            data["data"]+=i.encode('utf-8')+b":"+t[i].encode('utf-8')+b";"
        return data
    
    def apply_recv(self, data):
        d = data["data"].decode('utf-8')
        data["data"] = {}
        for i in d.split(";"):
            ia=i.split(":")
            if ':' not in i: continue
            j=utils.base64_decode(ia[0])
            data["data"][j] = utils.base64_decode(ia[1])
            try:
                data["data"][j] = json.loads(data["data"][j])
            except:
                pass
        return data
