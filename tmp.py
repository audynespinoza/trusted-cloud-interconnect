
# ---------------------
# +1 ip address on each ansible host
# ---------------------

hosts = '''[aln_wan]
alnwan1 ansible_host=192.168.122.1
alnwan2 ansible_host=192.168.122.2

[mck_wan]
mckwan1 ansible_host=192.168.122.3
mkcwan2 ansible_host=192.168.122.1

[ash_wan]
ashwan1 ansible_host=192.168.122.1
ashwan2 ansible_host=192.168.122.1
ashwan3 ansible_host=192.168.122.1
ashwan4 ansible_host=192.168.122.1

[aln_core]
alncore1 ansible_host=192.168.122.1
alncore2 ansible_host=192.168.122.1

[mck_core]
mckcore1 ansible_host=192.168.122.1
mckcore2 ansible_host=192.168.122.1

[ash_core]
ashcore1 ansible_host=192.168.122.1
ashcore2 ansible_host=192.168.122.1

[aln_fab]
alnfab1 ansible_host=192.168.122.1
alnfab2 ansible_host=192.168.122.1

[mck_fab]
mckfab1 ansible_host=192.168.122.1
mckfab2 ansible_host=192.168.122.1

[ash_cld]
ashcld1 ansible_host=192.168.122.1
ashcld2 ansible_host=192.168.122.1

[aln_fw]
alnfw1 ansible_host=192.168.122.1

[mck_fw]
mckfw1 ansible_host=192.168.122.1

[ash_fw]
ashfw1 ansible_host=192.168.122.1

[aln_trust]
alntrust1 ansible_host=192.168.122.1

[mck_trust]
mcktrust1 ansible_host=192.168.122.1

[ash_trust]
mcktrust1 ansible_host=192.168.122.1

[aln_nontrust]
alntrust1 ansible_host=192.168.122.1

[mck_nontrust]
mcktrust1 ansible_host=192.168.122.1

[ash_nontrust]
ashtrust1 ansible_host=192.168.122.1'''.splitlines()

x = 1
for i in hosts:
    if '192.168.122' in i:
        split_line = i.split('=')
        ip = split_line[-1]
        split_ip = ip.split('.')
        new_ip = '{}.{}'.format('.'.join(split_ip[:3]), x)
        x += 1
        print('{}={}'.format(split_line[0], new_ip))
    else:
        print(i)

# ansible-playbook pb_net_apply.yml


  - name: Create VRFs and Associate to Interfaces
    cisco.ios_ios_vrf:
    - name: "{{ item.name }}"
      description: "{{ item.description }}"
      rd: "{{ item.rd }}"
      route_both: "{{ item.route_both }}"
      interfaces: "{{ l3_interfaces[inventory_hostname] | selectattr('vrf', 'equalto', {{ item.vrf }}) | map(attribute='name') | list }}"
    loop: "{{ vrfs }}"
    notify: save_ios