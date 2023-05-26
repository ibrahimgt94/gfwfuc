from server import threaded_server

lisen_port = 4501
lisen_host = "127.0.0.1"

print ("** listen_at_host: {0} and port: {1}".format(lisen_host, lisen_port))
threaded_server(lisen_host, lisen_port).listen({
    "number_fragment": 78,
    "fragment_sleep": 0.02,
    "socket_timeout": 21,
    "first_time_sleep": 0.1,
    "accept_time_sleep": 0.01,
    "dns_cache_sec": 60,
    "run_cache_sec": 30000,
    "priority_offline": True,
    "delete_cache_dns": False,
    "cache_dns_override": False,
    "usa_dns_from_fragment": True,
    "usa_dns_speed": False,
    "clflr_cache_time": 30,
    "clflr_range": {
        "66.235.200.0"
    },
    "def_clflr_ip": "104.24.177.36",
    "worker_domain": "spring-block-4424.jklwebfgvweigbfch.workers.dev",
    "lisen_host": lisen_host,
    "lisen_port": lisen_port,
})