#!/usr/bin/env python
# coding=utf-8
# copy and paste from
# https://github.com/cokebar/gfwlist2dnsmasq
# https://github.com/JinnLynn/genpac
#
# how to:
# gfwlist2dnsmasqpy -i gfwlist -d 127.0.0.1 -p 1053 -o gfw.conf
#
#
# just skip -l in normal case, direct fetch from github
# -l="/path/to/gfwlist.txt" if your want use local raw gfwlist
#
# -ipset "your_ipset_name"
# -ipset - skip generate ipset rule
#
# -d "your_dns_ip"
#
# -p "your_dns_port"
#
# -o "output_file"
# -o - just print on stdout
#
#
from __future__ import print_function
import urllib2
import re
import os
import datetime
import base64
import argparse
import codecs
import StringIO
import sys


GFWLIST_URL = \
    'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'

# Extra Domain;
EX_DOMAIN = [
]


def fetch_gfwlist(local_path):
    content = None
    if local_path:
        try:
            with codecs.open(abspath(local_path), 'r', 'utf-8') as fp:
                raw = base64.decodestring(fp.read())
                content = StringIO.StringIO(raw)
        except:
            error('base64 decode fail.', exit=True)
    else:
        try:
            resp = urllib2.urlopen(GFWLIST_URL, timeout=10)
            content = StringIO.StringIO(resp.read().decode('base64'))
        except:
            error('fetch gfwlist fail.', exit=True)
    return content


def generate(gfwlist, ipset_name, dns_ip, dns_port):
    # the url of gfwlist
    # match comments/title/whitelist/ip address
    comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'
    ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')

    domainlist = []

    output = []
    output.append('# gfwlist rules for dnsmasq')
    output.append('# you can get it online')
    output.append('# go https://github.com/fpfeng/g2w.online')
    output.append('# ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    for line in gfwlist.readlines():
        if re.findall(comment_pattern, line):
            continue
        domain = re.findall(domain_pattern, line)
        if domain:
            try:
                _ = domainlist.index(domain[0])
            except ValueError:
                if ip_pattern.match(domain[0]):
                    continue
                domainlist.append(domain[0])
                append_domain(output, domain[0], dns_ip, dns_port)
                check_append_ipset(output, ipset_name, domain[0])

    for each in EX_DOMAIN:
        append_domain(output, each, dns_ip, dns_port)
        check_append_ipset(output, ipset_name, each)

    output.append('# end\n')
    return output


def append_domain(output_list, domain, dns_ip, dns_port):
    output_list.append('server=/.%s/%s#%s' % (domain, dns_ip, dns_port))


def check_append_ipset(output_list, ipset_name, domain):
    if ipset_name != '-':
        output_list.append('ipset=/.%s/%s' % (domain, ipset_name))


def abspath(path):
    if not path:
        return path
    if path.startswith('~'):
        path = os.path.expanduser(path)
    return os.path.abspath(path)


def error(*args, **kwargs):
    print(*args, file=sys.stderr)
    if kwargs.get('exit', False):
        sys.exit(1)


def get_args():
    parser = argparse.ArgumentParser(
        description='Generate a list of dnsmasq rules for gfwlist')
    parser.add_argument('-l', '--local', type=str)
    parser.add_argument('-i', '--ipset', type=str, required=True)
    parser.add_argument('-d', '--dnsip', type=str, required=True)
    parser.add_argument('-p', '--dnsport', type=int, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    args = parser.parse_args()
    local_path = args.local
    ipset_name = args.ipset
    dns_ip = args.dnsip
    dns_port = args.dnsport
    output_path = args.output
    return local_path, ipset_name, dns_ip, dns_port, output_path


def main():
    local_path, ipset_name, dns_ip, dns_port, output_path = get_args()
    gfwlist = fetch_gfwlist(local_path)
    output = generate(gfwlist, ipset_name, dns_ip, dns_port)
    file = '\n'.join(output)
    if output_path == '-':
        return sys.stdout.write(file)
    else:
        try:
            with codecs.open(abspath(output_path), 'w', 'utf-8') as fp:
                fp.write(file)
        except Exception:
            error('write output file fail.', exit=True)

if __name__ == '__main__':
    main()
