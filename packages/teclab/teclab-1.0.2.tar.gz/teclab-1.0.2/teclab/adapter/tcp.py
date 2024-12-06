# TCP协议适配器
# VERSION:1.0.0
# DATE:2024-12-1
# BY:杨浩天

import socket   
import time
import threading
from ping3 import ping

verify_msg=b"<Teclab-adapter-tcp_server-v1.0.0>"
heartbeat_msg=b"<heartbeat>"
local_servers=["192.168.x.x"]
central_servers=[
    'gateway.teclab.org.cn',
    'cms.teclab.org.cn',
    'central.teclab.org.cn',
    'gateway.yht.life',
    'cms.yht.life',
    'central.yht.life',
]

class server:
    def __init__(self,host="0.0.0.0",port=10000,logger=None):
        """TCP Server Adapter

        Args:
            host (str): bind host
            port (int): bind port
        """
        if ":" in host:
            host=host.split(":")
            port=host[1]
            host=host[0]
        self.host=host
        self.port=int(port)
        self.logger=logger
        self.channels=[]
        self.channels_id=0
        self.msg_cache={
            "send":[],
            "recv":[]
        }
        self.msg_start=b"[[st"
        self.msg_end=b"nd]]"
    
    def start(self):
        """Start the server
         Returns:
            tuple: (recv,send)
        """
        self.socket = socket.socket() 
        self.socket.bind((self.host, self.port))
        self.socket.listen(1000)
        self.socket.setblocking(False)
        t1=threading.Thread(target=self.accept_conn)
        t1.daemon=True
        t1.start()
        t2=threading.Thread(target=self.recv_handler)
        t2.daemon=True
        t2.start()
        t3=threading.Thread(target=self.send_handler)
        t3.daemon=True
        t3.start()
        return self
    
    def stop(self):
        """Stop the server
        """
        self.socket.close()
    
    def recv(self,block=False):
        """接收一个消息报文.
        
        Args:
            block (bool): 是否阻塞
        
        Returns:
            int: 通道id
            bytes: 消息报文
        """
        if block:
            while len(self.msg_cache["recv"])==0:
                time.sleep(0.01)
        return self.msg_cache["recv"].pop(0) if len(self.msg_cache["recv"])>0 else False
    
    def send(self,data,block=True):
        """发送一个消息报文.
        Args:
            data (bytes): 消息报文
            block (bool): 是否阻塞
        """
        self.msg_cache["send"].append(data)
        if block:
            while data in self.msg_cache["send"]:
                time.sleep(0.01)
        return True
    
    def accept_conn(self):
        """Accept the connection
        """
        while True:
            try:
                conn, addr = self.socket.accept()
                conn.setblocking(False)
                conn.send(verify_msg)
            except Exception as e:
                time.sleep(0.01)
                continue
            self.channels_id+=1
            self.channels.append({
                "id":self.channels_id,
                "conn":conn,
                "recv_cache":b"",
                "last_send_time":time.time()
            })
            time.sleep(0.01)
            if self.socket.fileno()==-1:
                if self.logger != None:
                    self.logger.ERROR("Server closed.")
                return
    
    def recv_handler(self):
        """Handler connections
        """
        while True:
            # 读取数据
            for channel in self.channels:
                # 读取数据
                try:
                    channel["recv_cache"] += channel["conn"].recv(1024*1024*10)
                except Exception as e:
                    if "[Errno 104]" in str(e) or "[WinError 10054]" in str(e):
                        if self.logger: self.logger.TRACE("Connection closed. IP:",channel["conn"].getpeername())
                        if channel in self.channels: del self.channels[self.channels.index(channel)]
                        time.sleep(0.01)
                        continue
                if self.msg_start in channel["recv_cache"] and self.msg_end in channel["recv_cache"]:
                    self.msg_cache["recv"].append({
                        "channel":channel["id"],
                        "data":channel["recv_cache"][channel["recv_cache"].index(self.msg_start)+len(self.msg_start):channel["recv_cache"].index(self.msg_end)]
                    })
                    channel["recv_cache"]=channel["recv_cache"][channel["recv_cache"].index(self.msg_end)+len(self.msg_end):]
            time.sleep(0.01)

    def send_handler(self):
        while True:
            # 发送数据
            for msg in self.msg_cache["send"]:
                # 找到self.channels里id为msg["id"]
                for channel in self.channels:
                    if channel["id"]==msg["channel"]:
                        break
                # 如果连接断开
                try:
                    channel["conn"].send(self.msg_start+msg["data"]+self.msg_end)
                    channel["last_send_time"]=time.time()
                except:
                    if self.logger: self.logger.TRACE("Connection closed. IP:",channel["conn"].getpeername())
                    if channel in self.channels: del self.channels[self.channels.index(channel)]
                self.msg_cache["send"].remove(msg)
            #　发送心跳包
            for channel in self.channels:
                if time.time()-channel["last_send_time"]>1:
                    try:
                        channel["conn"].send(heartbeat_msg)
                        channel["last_send_time"]=time.time()
                    except:
                        if self.logger: self.logger.TRACE("Connection closed. IP:",channel["conn"].getpeername())
                        if channel in self.channels: del self.channels[self.channels.index(channel)]
            time.sleep(0.01)
            
            
class client:
    def __init__(self,host="127.0.0.1",port=10000,logger=None):
        """TCP Client Adapter

        Args:
            host (str): host
            port (int): port
        """
        if ":" in host:
            host=host.split(":")
            port=host[1]
            host=host[0]
        self.host=host
        self.port=int(port)
        self.recv_cache=b""
        self.logger=logger
        self.destroyed=False
        self.msg_cache={
            "send":[],
            "recv":[]
        }
        self.msg_start=b"[[st"
        self.msg_end=b"nd]]"
        
    def start(self):
        """Start the client
        """
        self.socket = socket.socket() 
        self.socket.connect((self.host, self.port),)
        self.socket.setblocking(False)
        self.recv_thread=threading.Thread(target=self.recv_handler)
        self.recv_thread.daemon=True
        self.recv_thread.start()
        self.send_thread=threading.Thread(target=self.send_handler)
        self.send_thread.daemon=True
        self.send_thread.start()
        self.deamon_thread=threading.Thread(target=self.daemon)
        self.deamon_thread.daemon=True
        self.deamon_thread.start()
        return self
    
    def daemon(self):
        while self.send_thread.is_alive() and self.recv_thread.is_alive() and not self.destroyed:
            time.sleep(0.1)
        self.destroy()
        
    def stop(self):
        """Stop the client
        """
        self.destroyed=True
        self.socket.close()
    
        
    def recv(self,block=True):
        """接收一个消息报文.
        
        Args:
            block (bool): 是否阻塞
        
        Returns:
            int: 通道id
            bytes: 消息报文
        """
        if block:
            while len(self.msg_cache["recv"])==0:
                time.sleep(0.01)
        return self.msg_cache["recv"].pop(0) if len(self.msg_cache["recv"])>0 else False
    
    def send(self,data,block=True,timeout=10):
        """发送一个消息报文.
        Args:
            data (bytes): 消息报文
            block (bool): 是否阻塞
        """
        self.msg_cache["send"].append(data)
        if block:
            start_waiting_time=time.time()
            while data in self.msg_cache["send"]:
                time.sleep(0.01)
                if time.time()-start_waiting_time>timeout:
                    raise Exception("Send timeout.")
        return True
    
    def recv_handler(self):
        """Handler connections
        """ 
        self.last_recv_time=time.time()
        while True:
            if self.destroyed:
                return
            # 读取数据
            try:
                d=self.socket.recv(1024*1024*10)
                self.recv_cache += d
                if len(d)>0:
                    self.last_recv_time=time.time()
            except BlockingIOError:
                time.sleep(0.01)
                continue
            if time.time()-self.last_recv_time>5:
                if self.logger: self.logger.TRACE("Connection timeout.")
                raise Exception("Connection timeout.")   
            if self.msg_start in self.recv_cache and self.msg_end in self.recv_cache:
                self.msg_cache["recv"].append({
                    "channel":0,
                    "data":self.recv_cache[self.recv_cache.index(self.msg_start)+len(self.msg_start):self.recv_cache.index(self.msg_end)]
                })
                self.recv_cache=self.recv_cache[self.recv_cache.index(self.msg_end)+len(self.msg_end):]
                
    def send_handler(self):
        while True:
            if self.destroyed:
                return
            # 发送数据
            for msg in self.msg_cache["send"]:
                try:
                    self.socket.send(self.msg_start+msg["data"]+self.msg_end)
                except Exception as e:
                    continue
                self.msg_cache["send"].remove(msg)
            time.sleep(0.01)
            

class scanner:
    def __init__(self,local=local_servers,central=central_servers,callback=None,local_timeout=0.5,central_timeout=3):
        """扫描器

        Args:
            local (bool, optional): 扫描本地局域网. 
            central (bool, optional): 扫描中央服务器.
        """
        self.local=local
        self.central=central
        self.callback=callback
        self.servers=[]
        self.central_timeout=central_timeout
        self.local_timeout=local_timeout
        self.running_threads=0
        self.max_threads=1000
        self.stopped=False
        
    def scan(self):
        """扫描
        """
        t1=threading.Thread(target=self.scan_local,args=(self.local,))
        t1.daemon=True
        t1.start()
        t2=threading.Thread(target=self.scan_central,args=(self.central,))
        t2.daemon=True
        t2.start()
        if not self.callback:
            t1.join()
            t2.join()
            while self.running_threads>0:
                time.sleep(0.01)
        return self.servers
    
    def stop(self):
        """停止扫描
        """
        self.stopped=True
    
    def scan_local(self,servers):
        """扫描本地局域网
        """
        for ip in servers:
            if 'x' in ip:
                try:
                    r=ping(ip.replace('x','1'),timeout=self.local_timeout)
                except:
                    continue
                t_servers=[]
                for i in range(256):
                    t_servers.append(ip.replace('x',str(i),1))
                self.scan_local(t_servers)
            else:
                self.wait()
                t=threading.Thread(target=self.check,args=(ip,10000,self.local_timeout))
                t.daemon=True
                t.start()
    
    def scan_central(self,servers):
        """扫描中央服务器
        """
        for ip in servers:
            self.wait()
            t=threading.Thread(target=self.check,args=(ip,10000,self.central_timeout))
            t.daemon=True
            t.start()
    
    def wait(self):
        """等待扫描完成
        """
        while self.running_threads>self.max_threads:
            if self.stopped:
                raise Exception("Scan stopped.")
            time.sleep(0.01)
    
    def check(self,ip,port,timeout):
        """检查一个ip和端口是否开放
        """
        self.running_threads+=1
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((ip, port))
            cache=b""
            start_time=time.time()
            while time.time()-start_time<timeout:
                cache+=s.recv(1024*1024*10)
                if verify_msg in cache:
                    self.servers.append(ip)
                    self.callback(ip)
                    self.running_threads-=1
                    return True
        except:
            pass
        self.running_threads-=1
        return False
    