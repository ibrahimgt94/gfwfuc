import random

class conf(object):
    def __init__(self, conf):
        self.conf = conf

    def dns_uri(self):
        return {
            "1.1.1.1",
            # "1.0.0.1",
            # "8.20.247.2",
            # "167.114.220.125",
            # "163.172.34.56",
        }

    def redic_tube_uri(self):
        return random.choice(list({
            "instagram.fevn6-5.fna.fbcdn.net"
        }))

    def number_fragment(self):
        return self.conf.get("number_fragment")

    def fragment_sleep(self):
        return self.conf.get("fragment_sleep")

    def get_sleep_time(self):
        return self.conf.get("accept_time_sleep")
    
    def get_socket_timeout(self):
        return self.conf.get("socket_timeout")
    
    def lisen_host(self):
        return self.conf.get("lisen_host")

    def lisen_port(self):
        return self.conf.get("lisen_port")
    
    def save_cache_sec(self):
        return self.conf.get("dns_cache_sec")
    
    def run_cache_sec(self):
        return self.conf.get("run_cache_sec")

    def override_cache(self):
        return self.conf.get("override_cache")

    def cache_dns_override(self):
        return self.conf.get("cache_dns_override")

    def delete_cache_dns(self):
        return self.conf.get("delete_cache_dns")

    def get_priority(self):
        return self.conf.get("priority")

    def get_first_time_sleep(self):
        return self.conf.get("get_first_time_sleep")

    def usa_dns_from_fragment(self):
        return self.conf.get("usa_dns_from_fragment")

    def usa_dns_speed(self):
        return self.conf.get("usa_dns_speed")

    def get_proxy(self):
        return (self.conf.get("lisen_host"), self.conf.get("lisen_port"))

    def clflr_cache_time(self):
        return self.conf.get("clflr_cache_time")
    
    def clflr_range(self):
        return self.conf.get("clflr_range")

    def def_clflr_ip(self):
        return self.conf.get("def_clflr_ip")
    
    def get_worker_domain(self):
        return self.conf.get("worker_domain")