from scapy.layers.tls.all import *
from scapy.all import *
import requests
from ping3 import ping as ping3_ip


class ether(object):
    def __init__(self, conf, doh):
        self.reqs = requests.session()
        self.clflr = []
        self.clflr_ip = {}
        self.conf = conf
        self.doh = doh
    
    def get_sni(self, data):
        data = TLS(data)
        tls_ext = data[TLS].msg[0][TLS_Ext_ServerName][0]
        return tls_ext[ServerName].servername.decode()

    def exists_header_clflr(self, host):
        resp = self.reqs.get(f"https://{host}")
        return resp.headers.get("Server") == "cloudflare"

    def check_work_ip(self, addr):
        ping_time = ping3_ip(addr)
        if math.ceil(ping_time) != 0:
            ping_time = format(ping_time, ".3g")
            return ping_time
        return False

    def get_proxy_info(self):
        proxy_host, proxy_prot = self.conf.get_proxy()
        self.reqs.proxies = {'http': f'http://{proxy_host}:{proxy_prot}'}

    def header_args(self):
        return {
            "accept": "text/html"
        }

    def check_work_ip_sni(self, addr, domain):
        print ("check_work_ip_sni")
        proxies = self.get_proxy_info()
        header_args = self.header_args()
        try:
            resp = self.reqs.get(f"https://{domain}", headers=header_args)
            return addr
        except Exception as err:
            return False

    def clflr_range_ping(self, domain):
        try:
            clflr_range = self.conf.clflr_range()
            for clflr_ip in clflr_range:
                clflr_ip = clflr_ip.split(".")[:-1]
                for num in range(1, 255):
                    clflr_tmp = []
                    clflr_tmp = copy.deepcopy(clflr_ip)
                    clflr_tmp.append(str(num))
                    clflr_tmp = ".".join(clflr_tmp)
                    self.clflr_ip[domain] = clflr_tmp
                    work_ip_sni = self.check_work_ip_sni(clflr_tmp, domain)
                    if work_ip_sni != False:
                        self.doh.cache[domain] = work_ip_sni
                        return work_ip_sni

        except Exception as err:
            print("** clflr range not ping")
            return self.conf.def_clflr_ip()

    def check_clflr(self, data):
        host = self.get_sni(data)
        if host in self.clflr:
            if host in self.clflr_ip:
                clflr_ip = self.clflr_ip.get(host)
            else:
                clflr_ip = self.clflr_range_ping(host)
        else:
            is_clflr = self.exists_header_clflr(host)
            if is_clflr:
                self.clflr.append(host)
                clflr_ip = self.doh.query(host)
                chip = self.check_work_ip(clflr_ip)
                if chip != False:
                    self.clflr_ip[host] = clflr_ip
                else:
                    clflr_ip = self.clflr_range_ping(host)

        return (host, 443)