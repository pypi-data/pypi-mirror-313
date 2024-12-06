"""测试文件
"""

import time
import threading
from teclab import utils,adapter,client,server

id,secret=utils.generate_device()
serv=server.Server(id,secret,"",["tcp://0.0.0.0:10000"])
t=threading.Thread(target=serv.start)
t.daemon=True
t.start()

time.sleep(1)
print()
cli=client.Client(address="tcp://192.168.1.10:10000",SECRET=utils.generate_secret(secret,utils.raw2acc('1'*len(serv.mount_map))))
cli.start()
print("***")
print(cli.request("sys.echo",{"text":"Hello World!"})[1]["text"])
print("***")