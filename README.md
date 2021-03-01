# TLS Poison
Modified from https://github.com/jmdx/TLS-poison. Have pruned the original repo. Use two vps to reproduce the attack tech.



###	New DNS Alternater

```
python3 alternate-dns.py example.com --ip x.x.x.x --mode static_zero
Usage:
     --ip 					 Your vps ip or an ip which you want the domain point to.
     --static_zero   In this mode, the tool will return two A records in a DNS query. One of the records is your vps ip, the other one is 0.0.0.0.
     --rebinding		 In this mode, the tool will only return an A records in a DNS query. But it will randomly return 127.0.0.1 or the ip you set. Similar like the original alternate-dns tool.
```

