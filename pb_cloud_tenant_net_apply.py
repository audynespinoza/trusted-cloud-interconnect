---
# -------------------------------------
# Play - Configure Cloud Tenant Network 
# -------------------------------------
- name: Configure Cloud Tenant Network 
  hosts: cld
  tags: tenant_network_interface
  gather_facts: no
  tasks:
  - name: Create VRF
    cisco.ios.ios_vrf:
      name: "{{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}"
      description: "{{ item.description }}"
      state: present
    loop: "{{ tenant_networks }}"
    tags:
    - vrf
    notify: save_cfg
    ignore_errors: true
    ignore_unreachable: true

  - name: Configure Transit Network Interface
    cisco.ios.ios_interfaces:
      config:
      - name: "{{ item.interface }}"
        description: "{{ item.description }}"
      state: merged
    tags:
    - interface
    - physical
    loop: "{{ tenant_networks }}"
    notify: save_cfg
    ignore_errors: true
    ignore_unreachable: true

  - name: Associate Interface to VRF
    cisco.ios.ios_config:
      lines:
      - vrf forwarding {{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}
      parents:
      - interface {{ item.interface }}
    loop: "{{ tenant_networks }}"
    tags:
    - vrf_interface
    notify: save_cfg
    ignore_errors: true
    ignore_unreachable: true

  - name: Assign IPv4 Address to Interface On Primary
    cisco.ios.ios_l3_interfaces:
      config: 
      - name: "{{ item.interface }}"
        ipv4:
        - address: "{{ item.primary_transit_cidr | ipv4(item.primary_transit_local_ip_index) }}" 
    loop: "{{ tenant_networks }}"
    when:
    - ebgp_prepend_route_policy |
        selectattr('role', 'equalto', 'primary')
        map(attribute='devices') | flatten |
        selectattr('name', 'equalto', inventory_hostname)
    tags:
    - ip_address
    - interface
    notify: save_cfg
    ignore_errors: true
    ignore_unreachable: true

  - name: Assign IPv4 Address to Interface On Secondary
    cisco.ios.ios_l3_interfaces:
      config: 
      - name: "{{ item.interface }}"
        ipv4:
        - address: "{{ item.secondary_transit_cidr | ipv4(item.secondary_transit_local_ip_index) }}" 
    loop: "{{ tenant_networks }}"
    when:
    - ebgp_prepend_route_policy |
        selectattr('role', 'equalto', 'secondary')
        map(attribute='devices') | flatten |
        selectattr('name', 'equalto', inventory_hostname)
    tags:
    - ip_address
    - interface
    notify: save_cfg
    ignore_errors: true
    ignore_unreachable: true

  - name: Interface Admin State
    cisco.ios.ios_interfaces:
      config:
      - name: "{{ item.interface }}"
        enabled: "{{ item.enabled }}"
    loop: "{{ tenant_networks }}"
    tags:
    - admin_state
    notify: save_cfg
    ignore_errors: true
    ignore_unreachable: true

  handlers:
  - name: save_cfg
    ios_command:
      commands:
      - write mem
    when: not ansible_check_mode

# -------------------------------------------------
# Play - Configure iBGP Route Policy - CLD Layer
# -------------------------------------------------
- name: Configure eBGP Route Policy - CLD Layer
  hosts: cld
  tags: bgp_route_policy
  gather_facts: no
  tasks:
  - name: Configure Prefix-List for Public Cloud Networks
    cisco.ios.ios_prefix_lists:
      config:
        - afi: ipv4
          prefix_lists:
            - name: "{{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}"
              entries:
              - action: permit
                prefix: "{{ item.tenant_cidr }}"
                sequence: 1000
      state: merged
    loop: "{{ tenant_networks }}"
    tags:
    - ebgp_route_policy
    notify: save_cfg
    ignore_errors: true
    ignore_unreachable: true

  - name: Configure eBGP Route Policy - CLD To/From AWS Layer - Match Community
    cisco.ios.ios_route_maps:
      config:
      - route_map: "{{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}_OUT"
        entries:
        - sequence: 1000
          action: permit
          match:
            ip:
              address:
                prefix_lists:
                - 'DEFAULT'
      - route_map: "{{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}_IN"
        entries:
        - sequence: 1000
          action: permit
          match:
            ip:
              address:
                prefix_lists:
                - "{{ item.provider|upper }}-{{ item.description|upper }}"
      state: merged
    loop: "{{ tenant_networks }}"
    tags:
    - ebgp_route_policy
    notify: save_cfg
    ignore_errors: true
    ignore_unreachable: true

  - name: Configure eBGP Route Policy - CLD To Public Cloud Layer - Set AS-Path Prepending
    cisco.ios.ios_config:
      lines:
      - "set as-path prepend last-as {{ ebgp_prepend_route_policy |
                  selectattr('vrf', 'equalto', item.vrf) |
                  map(attribute='devices') | flatten |
                  selectattr('name', 'equalto', inventory_hostname) |
                  map(attribute='as_path_prepend') | join('') }}"
      parents: route-map "{{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}_OUT" permit 1000
    loop: "{{ tenant_networks }}"
    when:
    - ebgp_prepend_route_policy |
        map(attribute='devices') | flatten |
        selectattr('name', 'equalto', inventory_hostname) |
        map(attribute='as_path_prepend') | join('') in bgp_as_path_count_options
    tags:
    - ebgp_route_policy
    notify: save_cfg
    ignore_errors: true
    ignore_unreachable: true

  - name: Configure eBGP Route Policy - CLD To Public Cloud Layer - Remove AS-Path Prepending
    cisco.ios.ios_config:
      lines:
      - no set as-path prepend last-as
      parents: route-map "{{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}_OUT" permit 1000
    loop: "{{ tenant_networks }}"
    when:
    - ebgp_prepend_route_policy |
        map(attribute='devices') | flatten |
        selectattr('name', 'equalto', inventory_hostname) |
        map(attribute='as_path_prepend') | join('') not in bgp_as_path_count_options
    tags:
    - ebgp_route_policy
    notify: save_cfg
    ignore_errors: true
    ignore_unreachable: true


  - name: Configure eBGP Neighbor on Primary
    cisco.ios.ios_bgp_address_family:
      config:
        as_number: "{{ bgp.local_as }}"
        address_family:
        - afi: ipv4
          safi: unicast
          vrf: "{{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}"
          neighbor:
          - address: "{{ item.primary_transit_cidr | ipv4(item.primary_transit_peer_ip_index) | ipaddr('address') }}"
            activate: true
            remote_as: "{{ item.transit_peer_bgp_asn }}"
            timers:
              holdtime: "{{ bgp_holdtime }}"
              interval: "{{ bgp_keepalive_interval }}"
            soft_reconfiguration: true
            send_community:
              both: true
            password: "{{bgp_neighbor_pwd}}"
            route_maps:
              - name: "{{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}_OUT"
                out: true
              - name: "{{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}_IN"
                in: true
      state: merged
    loop: "{{ tenant_networks }}"
    when:
    - ebgp_prepend_route_policy |
        selectattr('role', 'equalto', 'primary')
        map(attribute='devices') | flatten |
        selectattr('name', 'equalto', inventory_hostname)
    tags:
    - bgp_neighbor
    notify: save_cfg
    ignore_errors: true
    ignore_unreachable: true

  - name: Configure eBGP Neighbor on Secondary
    cisco.ios.ios_bgp_address_family:
      config:
        as_number: "{{ bgp.local_as }}"
        address_family:
        - afi: ipv4
          safi: unicast
          vrf: "{{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}"
          neighbor:
          - address: "{{ item.secondary_transit_cidr | ipv4(item.secondary_transit_peer_ip_index) | ipaddr('address') }}"
            activate: true
            remote_as: "{{ item.transit_peer_bgp_asn }}"
            timers:
              holdtime: "{{ bgp_holdtime }}"
              interval: "{{ bgp_keepalive_interval }}"
            soft_reconfiguration: true
            send_community:
              both: true
            password: "{{bgp_neighbor_pwd}}"
            route_maps:
              - name: "{{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}_OUT"
                out: true
              - name: "{{ item.provider|upper }}_{{ item.description|upper }}_{{ item.region|upper }}_IN"
                in: true
      state: merged
    loop: "{{ tenant_networks }}"
    when:
    - ebgp_prepend_route_policy |
        selectattr('role', 'equalto', 'secondary')
        map(attribute='devices') | flatten |
        selectattr('name', 'equalto', inventory_hostname)
    tags:
    - bgp_neighbor
    notify: save_cfg
    ignore_errors: true
    ignore_unreachable: true

  handlers:
  - name: save_cfg
    ios_command:
      commands:
      - write mem
    when: not ansible_check_mode