from pprint import pprint

with open('hosts') as f:
    host_info = f.readlines()

host_entries = ''


for i in host_info:
    if 'ansible_host=' in i:
        name = i.split()[0].strip()
        ip = i.split('=')[-1].strip()
        host_entries += f'{ip} {name}\n'


with open('etc_hosts_entries.txt', 'w') as f:
    f.write(host_entries)
