"""测试文件
"""

import time
import threading
from teclab import utils,adapter,client,server

id,secret=utils.generate_device()
serv=server.Server(id,secret)
serv.init_adapters(adapters=[adapter.tcp.server().start()])
serv.init_middlewares()
t=threading.Thread(target=serv.start)
t.daemon=True
t.start()

time.sleep(1)
print()
cli=client.Client(adapter_=adapter.tcp.client("127.0.0.1",10000).start(),SECRET=utils.generate_secret(secret,utils.raw2acc('1'*len(serv.mount_map))))
print("***")
print(cli.request("sys.echo",{"text":"Hello World!"})[1]["text"])
print("***")