
# -------------------------------------------------------
# Play - Hostvars
# -------------------------------------------------------
- name: Configure Tenant Static Routes On Firewall Layer
  hosts: localhost
  tags: hostvars_output
  gather_facts: no
  tasks:
  - name: Hostvars output
    debug:
      var: hostvars




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



  - name: Configure BGP Redistribution
    cisco.ios.ios_bgp_address_family:
      config:
        as_number: "{{ bgp.local_asn }}"
        address_family:
        - afi: ipv4
          safi: unicast
          vrf: "{{ item.vrf }}"
          neighbor:
          - address: "{{ item.cidr | ipv4(not item.host_ip_index) | ipaddr('address') }}" 
            activate: true
            remote_as: "{{ bgp.local_asn }}"
            route_reflector_client: "{{ item.bgp_route_reflect }}"
            nexthop_self:
              all: false
              set: "{{ item.bgp_next_hop_self }}"
            timers:
              holdtime: "{{ bgp_holdtime }}"
              interval: "{{ bgp_keepalive_interval }}"
            soft_reconfiguration: true
            send_community:
              both: true
            password: "{{bgp_neighbor_pwd}}"
            route_maps:
              - name: "{{ item.description|upper }}_OUT_{{ item.vrf }}"
                out: true
              - name: "{{ item.description|upper }}_IN_{{ item.vrf }}"
                in: true
          redistribute:
            - connected:
                route_map: "CONN_BGP_{{ item.vrf }}"
            - static:
                route_map: "STATIC_BGP_{{ item.vrf }}"
      state: replaced
    loop: "{{
      l3_interfaces[inventory_hostname] |
      selectattr('bgp', 'equalto', true) |
      selectattr('bgp_type', 'equalto', 'internal') |
      list }}"
    tags:
    - ibgp
    notify: save_cfg



  - name: Display BGP Neighbor status
    debug: var=bgp_neighbor_status.results
    tags:
    - show_bgp_neighbors

OSPF
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



  - name: Configure iBGP Route Policy - WAN to WAN Layer
    cisco.ios.ios_route_maps:
      config:
      - route_map: "{{ item.description|upper }}_OUT_{{ item.vrf }}"
        entries:
        - sequence: 1000
          action: permit
          set:
            community:
              number: "{{ 
                vrfs |
                selectattr('name', 'equalto', item.vrf) |
                map(attribute='bgp_community_number') |
                join('') }}"
      state: merged
    loop: "{{
      l3_transit_interfaces[inventory_hostname] |
      selectattr('bgp', 'equalto', true) |
      list }}"
    when: "'wan' in hostvars[item.description].group_names"
    tags:
    - ibgp_route_policy
    notify: save_cfg


# --------------------------------------------------
# Play - Build Device Name to AS-Path Prepend Policy
# --------------------------------------------------
- name: Configure Site Based BGP Community-Lists
  hosts: aln_wan
  tags: route_policy
  gather_facts: no
  tasks:
  - name: Build Device Name to AS-Path Prepend Policy Map for Each Device
    set_fact:
      device_map: "{{ 
        device_map | default({}) |
        combine ({ inventory_hostname : item.bgp_local_as }) }}"
    loop: "{{ 
      bgp_prepend_route_policy|
      selectattr('cidr', 'defined') |
      list }}"
    tags:
    - build_ip_asn_map

  - name: Display the Dictionary
    debug: var=device_map
    tags:
    - build_ip_asn_map   

  - name: Combine Each Device Interface-IP to BGP ASN mappings 
    set_fact:
      ip_asn_map: "{{ ip_asn_map | default({}) | combine(item) }}"
    loop: "{{
          groups['all_devices'] |
          map('extract', hostvars) |
          selectattr('device_map', 'defined') |
          map(attribute='device_map') |
          list }}"
    tags:
    - build_ip_asn_map

  - name: Display Interface-IP to BGP ASN mappings 
    debug:
      var: ip_asn_map
    tags:
    - build_ip_asn_map



  - name: Configure eBGP Route Policy - WAN To WAN Layer - Set AS-Path Prepending
    cisco.ios.ios_config:
      lines:
      - "set as-path prepend last-as {{ bgp_prepend_route_policy |
                  selectattr('vrf','equalto',item.vrf) |
                  map(attribute='devices') | flatten |
                  selectattr('name','equalto',inventory_hostname) |
                  map(attribute='as_path_prepend') | join('') }}"
      parents: route-map "{{ item.description|upper }}_OUT_{{ item.vrf }}" permit 1000
    loop: "{{
      l3_transit_interfaces[inventory_hostname] |
      selectattr('bgp','equalto',true) |
      list }}"
    when:
    - "'wan' in hostvars[item.description].group_names"
    - hostvars[item.description].bgp.local_asn != item.bgp_local_as
    - bgp_prepend_route_policy |
        selectattr('vrf','equalto',item.vrf) |
        map(attribute='devices') | flatten |
        selectattr('name','equalto',inventory_hostname) |
        map(attribute='as_path_prepend') | join('') in bgp_as_path_length_options
    tags:
    - ebgp_route_policy
    - sweet
    notify: save_cfg


  - name: Configure eBGP Route Policy - WAN To WAN Layer - Remove AS-Path Prepending
    cisco.ios.ios_config:
      lines:
      - no set as-path prepend last-as
      parents: route-map "{{ item.description|upper }}_OUT_{{ item.vrf }}" permit 1000
    loop: "{{
      l3_transit_interfaces[inventory_hostname] |
      selectattr('bgp','equalto',true) |
      list }}"
    when:
    - "'wan' in hostvars[item.description].group_names"
    - hostvars[item.description].bgp.local_asn != item.bgp_local_as
    - bgp_prepend_route_policy |
        selectattr('vrf','equalto',item.vrf) |
        map(attribute='devices') | flatten |
        selectattr('name','equalto',inventory_hostname) |
        map(attribute='as_path_prepend') | join('') == 'no'
    tags:
    - ebgp_route_policy
    - sweet
    notify: save_cfg
