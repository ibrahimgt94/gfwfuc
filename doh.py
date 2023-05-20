import json
import conf
import random
import math
from ping3 import ping as ping3_ip
import requests as reqs

class doh(object):
    def __init__(self, conf):
        self.type_a = 1
        self.sucess = 200
        self.reqs = reqs.session()
        self.cache = {}
        self.conf = conf
        # self.uri = None
    
    def set_dns_uri(self, uri):
        self.uri = uri
    
    def set_dns_uri_rand(self):
        dns_uri = list(self.conf.dns_uri())
        rand_dns_uri = random.choice(dns_uri)
        print(f"** load_random_dns: {speed_dns}")
        self.set_dns_uri()

    def set_dns_uri_sort_speed(self):
        dns_uri = self.conf.dns_uri()
        ping_info = {}
        for uri in dns_uri:
            ping_info[uri] = self.check_work_ip(uri)
        ping_speed = sorted(ping_info.items(), key=lambda item: item[1])
        speed_dns = ping_speed[0][0]
        print(f"** load_speed_dns: {speed_dns}")
        self.set_dns_uri(speed_dns)

    def query_args(self, domain):
        return {
            "name": domain,
            "type": "A",
            "accept": "application/dns-json"
        }

    def header_args(self):
        return {
            "accept": "application/dns-json"
        }

    def dns_offline(self):
        return {
            'ocsp.pki.goog': '172.217.16.195',
            'googleads.g.doubleclick.net': '45.157.177.108',
            'fonts.gstatic.com': '142.250.185.227',
            'rr2---sn-vh5ouxa-hju6.googlevideo.com': '213.202.6.141',
            'jnn-pa.googleapis.com': '45.157.177.108',
            'static.doubleclick.net': '202.61.195.218', 
            'rr4---sn-hju7en7k.googlevideo.com': '74.125.167.74',
            'rr1---sn-hju7en7r.googlevideo.com': '74.125.167.87',
            'play.google.com': '142.250.184.238',
            'rr3---sn-vh5ouxa-hjuz.googlevideo.com': '134.0.218.206', 
            'rr3---sn-hju7enel.googlevideo.com': '74.125.98.40',
            'download.visualstudio.microsoft.com': '68.232.34.200',
            'ocsp.pki.goog': '172.217.16.195',
            'i.ytimg.com': '142.250.186.150',
            'rr2---sn-hju7enel.googlevideo.com': '74.125.98.39',
            'rr2---sn-hju7en7k.googlevideo.com': '74.125.167.72', 
            'googleads.g.doubleclick.net': '45.157.177.108',
            'rr3---sn-4g5lznl6.googlevideo.com': '74.125.173.40', 
            'jnn-pa.googleapis.com': '89.58.57.45', 
            'rr3---sn-hju7en7k.googlevideo.com': '74.125.167.73',
            'rr1---sn-hju7enll.googlevideo.com': '74.125.98.6',
            'rr6---sn-hju7en7r.googlevideo.com': '74.125.167.92',
            'play.google.com': '216.58.212.174',
            'www.gstatic.com': '142.250.185.99', 
            'apis.google.com': '172.217.23.110',
            'adservice.google.com': '202.61.195.218',
            'mail.google.com': '142.250.186.37', 
            'accounts.google.com': '172.217.16.205', 
            'lh3.googleusercontent.com': '193.26.157.66',
            'accounts.youtube.com': '172.217.16.206',
            'ssl.gstatic.com': '142.250.184.195', 
            'fonts.gstatic.com': '172.217.23.99', 
            'rr4---sn-hju7enll.googlevideo.com': '74.125.98.9',
            'rr2---sn-hju7enll.googlevideo.com': '74.125.98.7',
            'rr1---sn-hju7enel.googlevideo.com': '74.125.98.38',
            'rr5---sn-vh5ouxa-hjuz.googlevideo.com': '134.0.218.208', 
            'i1.ytimg.com': '172.217.18.14',
            'plos.org': '162.159.135.42', 
            'fonts.googleapis.com': '89.58.57.45',
            'genweb.plos.org': '104.26.1.141',
            'static.ads-twitter.com': '146.75.120.157',
            'www.google-analytics.com': '142.250.185.174',
            'rr1---sn-vh5ouxa-hju6.googlevideo.com': '213.202.6.140',
            'rr5---sn-vh5ouxa-hju6.googlevideo.com': '213.202.6.144',
            'rr3---sn-hju7enel.googlevideo.com': '74.125.98.40',
            'rr5---sn-nv47zn7y.googlevideo.com': '173.194.15.74', 
            'rr1---sn-vh5ouxa-hju6.googlevideo.com': '213.202.6.140',
            'safebrowsing.googleapis.com': '202.61.195.218',
            'static.doubleclick.net': '193.26.157.66',
            'rr5---sn-vh5ouxa-hju6.googlevideo.com': '213.202.6.144', 
            'rr1---sn-hju7en7r.googlevideo.com': '74.125.167.87',
            'rr4---sn-vh5ouxa-hju6.googlevideo.com': '213.202.6.143',
            'rr4---sn-hju7en7r.googlevideo.com': '74.125.167.90',
            'r1---sn-hju7enel.googlevideo.com': '74.125.98.38', 
            'rr1---sn-nv47zn7r.googlevideo.com': '173.194.15.38',
            'rr2---sn-vh5ouxa-hjuz.googlevideo.com': '134.0.218.205', 
            'rr4---sn-nv47zn7r.googlevideo.com': '173.194.15.41',
            'rr4---sn-hju7en7r.googlevideo.com': '74.125.167.90',
            'www.instagram.com': '157.240.252.174',
            'instagram.fevn4-1.fna.fbcdn.net': '185.57.71.161',
            'instagram.fevn4-2.fna.fbcdn.net': '185.150.166.97',
            'instagram.fevn4-3.fna.fbcdn.net': '178.219.57.34',
            'instagram.fevn6-5.fna.fbcdn.net': '178.160.243.224',
            'instagram.fevn6-6.fna.fbcdn.net': '178.160.242.97',
            'instagram.fevn7-1.fna.fbcdn.net': '82.199.196.225',
            'instagram.fevn8-1.fna.fbcdn.net': '195.191.186.35',
            'www.google.com': '142.250.186.36',
            'youtube.com':'216.239.38.120',
            'www.youtube.com':'216.239.38.120',
            'i.ytimg.com':'216.239.38.120',
            'yt3.ggpht.com': '142.250.186.36',
        }

    def get_proxy_info(self):
        if self.conf.usa_dns_from_fragment() == True:
            proxy_host, proxy_prot = self.conf.get_proxy()
            self.reqs.proxies = {'http': f'http://{proxy_host}:{proxy_prot}'}

    def send_reqs_resl_dns(self, uri_api_ser, domain):
        proxies = self.get_proxy_info()
        query_args = self.query_args(domain)
        header_args = self.header_args()
        return self.reqs.get(uri_api_ser, params=query_args, headers=header_args)       

    def gens_dns_uri(self, host_dns_ser, domain):
        return "https://{0}/dns-query?name={1}".format(host_dns_ser, domain)

    def check_status_code(self, resp):
        return (resp.status_code == self.sucess)

    def get_offline(self, domain):
        return self.dns_offline().get(domain)
    
    def get_cache(self, domain):
        return self.cache.get(domain)

    def get_all_cache(self):
        return self.cache

    def add_cache(self, domain, addr):
        ping_time = self.check_work_ip(addr)
        if ping_time:
            self.cache[domain] = {"addr": addr, "ping": ping_time}

    def override_cache(self, cache):
        self.cache = json.loads(cache)

    def check_work_ip(self, addr):
        ping_time = ping3_ip(addr)
        if math.ceil(ping_time) != 0:
            ping_time = format(ping_time, ".3g")
            return ping_time
        return False

    def query(self, domain, conf):
        ip_offline = self.get_offline(domain)
        ip_cache = self.get_cache(domain)
        if ip_cache != None:
            ip_cache =ip_cache.get("addr")

        if conf.get_priority() == True:
            if ip_offline:
                self.add_cache(domain, ip_offline)
                return ip_offline
            elif ip_cache:
                return ip_cache
        else:
            if ip_cache:
                return ip_cache
            elif ip_offline:
                self.add_cache(domain, ip_offline)
                return ip_offline
        
        dns_uri_api = self.gens_dns_uri(self.uri, domain)
        resp = self.send_reqs_resl_dns(dns_uri_api, domain)
        if self.check_status_code(resp):
            return self.get_answer(resp, domain)

    def get_answer(self, resp, domain):
        resp = resp.json()
        answers = resp.get('Answer')
        if answers:
            for answer in answers:
                if answer['type'] == self.type_a:
                    answer_ip = answer['data']
                    self.add_cache(domain, answer_ip)
                    return answer_ip
        return False
