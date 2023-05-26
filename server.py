import json
import socket
import requests
import random
import time
import os
from sock import sock
from conf import conf
from ether import ether
import threading
from doh import doh
from rtimer import rtimer


class threaded_server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = sock()

    def listen(self, conf_args):
        self.conf = conf(conf_args)
        self.doh = doh(self.conf)
        self.ether = ether(self.conf, self.doh)
        if self.conf.usa_dns_speed() == True:
            self.doh.set_dns_uri_sort_speed()
        else:
            self.doh.set_dns_uri_rand()
        self.thread(self.repet_timer)
        self.while_listen()
    
    def while_listen(self):
        timeout = self.conf.get_socket_timeout()
        host = self.conf.lisen_host()
        port = self.conf.lisen_port()
        cl_sock2 = self.sock.client(host, port, timeout)
        cl_sock2.listen()
        while True:
            cl_sock, cl_addr = cl_sock2.accept()
            timeout = self.conf.get_socket_timeout()
            cl_sock.settimeout(timeout)
            time.sleep(self.conf.get_sleep_time())
            
            data = cl_sock.recv(16384)

            if (data[:7] == b"CONNECT" or (data[:3]==b'GET') or (data[:4]==b'POST')):
                self.thread(self.up_stream, (cl_sock, data, True))
            else:
                timeout = self.conf.get_socket_timeout()
                ser_sock = self.sock.server(timeout)
                clflr_ser = self.conf.def_clflr_ip()
                ser_sock.connect((clflr_ser, 443))
                self.thread(self.while_up_stream, (cl_sock, ser_sock, data, False))                

    def up_stream(self, cl_sock, data, type):
        bk_sock = self.han_cl_reqs(cl_sock, data)
        if(bk_sock == None):
            cl_sock.close()
            return False
        self.while_up_stream(cl_sock, bk_sock, data, type)

    def get_info_ser(self, data):
        host_and_port = str(data).split()[1]
        host, port = host_and_port.split(':')
        return (host, int(port)) 

    def move_http_to_https(self, cl_sock, data):
        q_line = str(data).split('\r\n')
        q_url = q_line[0].split()[1]
        q_url = q_url.replace('http://','https://')  
        response_data = 'HTTP/1.1 302 Found\r\nLocation: '+q_url+'\r\nProxy-agent: MyProxy/1.0\r\n\r\n'            
        cl_sock.sendall(response_data.encode())
        cl_sock.close()            
        return None

    def send_bad_gateway(self, cl_sock):
        response_data = b'HTTP/1.1 502 Bad Gateway\r\nProxy-agent: MyProxy/1.0\r\n\r\n'
        cl_sock.sendall(response_data)

    def get_relv_ser_ip(self, ser_host):
        try:
            socket.inet_aton(ser_host)
            return ser_host
        except socket.error:
            return self.doh.query(ser_host)

    def send_conn_establis(self, cl_sock):
        response_data = b'HTTP/1.1 200 Connection established\r\nProxy-agent: MyProxy/1.0\r\n\r\n'            
        cl_sock.sendall(response_data)

    def han_cl_reqs(self, cl_sock, data):
        if data[:7] == b"CONNECT":
            ser_host, ser_port = self.get_info_ser(data)
        elif (data[:3]==b'GET') or (data[:4]==b'POST'):
            return self.move_http_to_https(cl_sock, data)

        timeout = self.conf.get_socket_timeout()
        ser_sock = self.sock.server(timeout)

        try:
            ser_ip = self.get_relv_ser_ip(ser_host)
            ser_sock.connect((ser_ip, ser_port))
            self.send_conn_establis(cl_sock)
            return ser_sock

        except Exception as e:
            self.send_bad_gateway(cl_sock)
            cl_sock.close()
            ser_sock.close()
            return None

    def while_up_stream(self, cl_sock, bk_sock, data, type = False):
        first = True
        try:
            while True:
                if first == True:
                    first = False
                    if type == True:
                        data = cl_sock.recv(16384)
                    if data:
                        self.thread(self.while_down_stream, (cl_sock, bk_sock))
                        self.fragment(bk_sock, data)
                else:
                    data = cl_sock.recv(16384)
                    if data:
                        bk_sock.sendall(data)
        except Exception as e:
            time.sleep(2)
            cl_sock.close()
            bk_sock.close()
            return False

    def fragment(self, bk_sock, data):
        L_data = len(data)
        num_fragment = self.conf.number_fragment()
        indices = random.sample(range(1,L_data-1), num_fragment-1)
        indices.sort()
        time.sleep(self.conf.fragment_sleep())
        i_pre=0
        for i in indices:
            fragment_data = data[i_pre:i]
            i_pre=i
            time.sleep(self.conf.fragment_sleep())
            bk_sock.sendall(fragment_data)
        fragment_data = data[i_pre:L_data]
        bk_sock.sendall(fragment_data)
        print('** fragment')

    def while_down_stream(self, cl_sock, bk_sock):
        first = True
        try:
            while True:
                if first == True:
                    first = False
                    data = bk_sock.recv(16384)
                    if data:
                        cl_sock.sendall(data)
                else:
                    data = bk_sock.recv(16384)
                    if data:
                        cl_sock.sendall(data)
        except Exception as e:
            time.sleep(2)
            cl_sock.close()
            bk_sock.close()
            return False

    def doh_serv(self):
        doh_uri = self.conf.dns_uri_rand()
        return doh.serv(doh_uri)

    def thread(self, target, args=()):
        thread_up = threading.Thread(target=target, args=args)
        thread_up.daemon = True
        thread_up.start()

    def save_cache_dns(self):
        fopen = open("dns_cache.txt","w+")
        chache_data = self.doh.get_all_cache()
        fopen.write(str(chache_data))
        fopen.close()
        print("** save_cache_to_file")

    def get_cache_dns_file(self):
        if self.conf.delete_cache_dns() == True:
            if os.path.exists("dns_cache.txt"):
                os.remove("dns_cache.txt")
                print("** delete_cache_file")

        elif self.conf.cache_dns_override() == True:
            fopen = open("dns_cache.txt","r")
            chache_data = fopen.read()
            self.conf.override_cache(chache_data)
            fopen.close()
            print("** read_cache_file")

    def repet_timer(self):
        cache_sec = self.conf.save_cache_sec()
        max_run_save_cache = self.conf.run_cache_sec()
        repet_timer = rtimer(cache_sec, self.save_cache_dns)
        try:
            time.sleep(max_run_save_cache)
        finally:
            repet_timer.stop()