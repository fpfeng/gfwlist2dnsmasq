gfwlist2dnsmasq
=================
Intro
-----
Just another script to auto-generate dnsmasq ipset rules using gfwlist

Using:
-----
### First git clone
```bash
git clone https://github.com/cokebar/gfwlist2dnsmasq.git
```
### Modify gfwlist2dnsmasq.sh:
#### Change this to your DNS server:
DNS='127.0.0.1#5353'

#### Change this to your ipset name:
IPSET=gfwlist

#### Path to save you rule file:
RULE_FILE=./dnsmasq_list.conf

#### Add your own extra domain here. One domain in a line. eg:
EX_DOMAIN='.google.com
.google.com.hk
.google.com.tw
.google.com.sg
.google.co.jp
.blogspot.com
.blogspot.sg
.blogspot.hk
.blogspot.jp
.gvt1.com
.gvt2.com
.gvt3.com
.1e100.net
.blogspot.tw'

### And then just cd to the directory and run gfwlist2dnsmasq.sh:
```bash
cd gfwlist2dnsmasq
./gfwlist2dnsmasq.sh
```