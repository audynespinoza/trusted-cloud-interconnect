from pprint import pprint

with open('hosts') as f:
    host_info = f.readlines()

acl_wildcard = '192.168.86.0 0.0.0.255'
default_gw = '192.168.86.1'

device_cfgs = ''

for i in host_info:
    if 'ansible_host=' in i:
        name = i.split()[0].strip()
        ip = i.split('=')[-1].strip()
        device_cfg = f'''
# ---------------------------------------------------
# {name.upper()}
# ---------------------------------------------------
enable
config t

hostname {name}

ip domain-name cciedev.io

username lab priv 15 secret cisco

ip access-list stan 99
permit {acl_wildcard}

line vty 0 15
access-class 99 in vrf-also
login local
trans input ssh

ip vrf MGT

int g0/0
no sw
ip vrf forwarding MGT
ip add {ip} 255.255.255.0
no sh

ip route vrf MGT 0.0.0.0 0.0.0.0 {default_gw}

cry key gen rsa
yes
2048

do wr

'''

        device_cfgs += device_cfg

print(device_cfgs)

with open('bootstrap.cfg', 'w') as f:
    f.write(device_cfgs)


