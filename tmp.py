
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


  - name: Inteface OSPF Configuration
    cisco.ios.ios_ospf_interfaces:
      config:
        - name: "{{ item.name }}"
          address_family:
            - afi: ipv4
              process:
                id: "{{ item.ospf_process }}"
                area_id: 0
              adjacency: true
              bfd: true
              cost:
                interface_cost: 5
              hello_interval: 1
              dead_interval:
                time: 5
              network:
                point_to_point: true
              
    loop: "{{ l3_interfaces[inventory_hostname] | selectattr('ospf_active', 'equalto', true) | list }}"
    tags:
    - ospf
    notify: save_cfg

  - name: Configure BGP parameters and iBGP neighbors
    cisco.ios.ios_bgp_address_family:
      config:
        as_number: "{{ local_asn }}"
        address_family:
          - afi: ipv4
            safi: unicast
            vrf: "{{ item.vrf }}"
            neighbor:
              - address: "{{ item.cidr | ipv4(item.host_ip_index) | ipaddr('address') }}" 
                remote_as: "{{ local_asn }}"
                route_map:
                  - name: test-route-out
                    out: true
                  - name: test-route-in
                    in: true
                route_server_client: true


      - name: Global OSPF configuration for VRF TRUSTED
    cisco.ios.ios_ospfv2:
      config:
        processes:
        - process_id: "{{ item.ospf_process }}"
          vrf: "{{ item.vrf }}"
          max_metric:
            router_lsa: true
            on_startup:
              time: 110
          areas:
          - area_id: '0'
            default_cost: 5
          network:
          - address: "{{ item.cidr | ipv4(item.host_ip_index) | ipaddr('address') }}" 
            wildcard_bits: 0.0.0.0
            area: '0'
          passive_interfaces:
            default: true
            interface:
              set_interface: false
              name:
              - "{{ item.name }}"
      state: merged
    loop: "{{
      l3_interfaces[inventory_hostname] |
      selectattr('ospf_active', 'equalto', true) |
      selectattr('ospf_process', 'equalto', '2') |
      list }}"
    tags:
    - ospf
    notify: save_cfg


  - name: Configure iBGP neighbors
    cisco.ios.ios_bgp_global:
      config:
        as_number: "{{ bgp.local_asn }}"
        bgp:
          router_id:
            address: "{{ 
              l3_interfaces[inventory_hostname] |
              selectattr('description', 'equalto', 'loopback') |
              selectattr('vrf', 'equalto', item.vrf) |
              map(attribute='cidr') | ipv4(item.host_ip_index) | ipaddr('address') | join('') }}"
            vrf: true
          log_neighbor_changes: "{{ bgp_log_neighbor_changes }}"
        neighbor:
          - activate: true
            address: "{{ item.cidr | ipv4(not item.host_ip_index|bool) | ipaddr('address') }}" 
            remote_as: "{{ bgp.local_asn }}"
            route_reflector_client: "{{ item.bgp_route_reflect }}"
            next_hop_self: "{{ item.bgp_next_hop_self }}"
            
            password: "{{ bgp_neighbor_pwd }}"
            send_community: 
              standard: true
            shutdown:
              set: "{{ not item.bgp_enabled|bool }}"
        redistribute:
          - connected:
              route_map: "CONN_BGP_{{ item.vrf }}"
          - static:
              route_map: "STATIC_BGP_{{ item.vrf }}"
          - vrf:
              name: "{{ item.vrf }}"
        timers:
          keepalive: "{{ bgp_keepalive_interval }}"
          holdtime: "{{ bgp_holdtime }}"
      state: merged
    loop: "{{
      l3_interfaces[inventory_hostname] |
      selectattr('bgp', 'equalto', true) |
      selectattr('bgp_type', 'equalto', 'internal') |
      list }}"
    tags:
    - ibgp
    notify: save_cfg

