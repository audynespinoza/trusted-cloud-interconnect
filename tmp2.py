  # --------
  # ashcore1
  # --------
  ashcore1:
  - name: Loopback0
    cidr: 10.224.3.3/32
    host_ip_index: 0
    vrf: GLOBAL
    description: main_loopback
    enabled: true
    underlay: false
    physical: false
    ospf_active: false
    ospf_process: 0
    bgp: false
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: no

  - name: Loopback1
    cidr: 10.224.113.3/32
    host_ip_index: 0
    vrf: CORE
    description: main_loopback
    enabled: true
    underlay: false
    physical: false
    ospf_active: true
    ospf_process: '1'
    bgp: false
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: false

  - name: Loopback2
    cidr: 10.224.123.3/32
    host_ip_index: 0
    vrf: TRUSTED
    description: main_loopback
    enabled: true
    underlay: false
    physical: false
    ospf_active: true
    ospf_process: '2'
    bgp: false
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: false

  - name: GigabitEthernet0/1
    cidr: 10.224.13.0/31
    host_ip_index: 1
    vrf: CORE
    description: ashwan1
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '1'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: GigabitEthernet1/1
    cidr: 10.224.23.0/31
    host_ip_index: 1
    vrf: TRUSTED
    description: ashwan1
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '2'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: GigabitEthernet0/2
    cidr: 10.224.13.4/31
    host_ip_index: 1
    vrf: CORE
    description: ashwan2
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '1'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: GigabitEthernet1/2
    cidr: 10.224.23.4/31
    host_ip_index: 1
    vrf: TRUSTED
    description: ashwan2
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '2'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: True

  - name: GigabitEthernet1/0
    cidr: 10.224.13.8/31
    host_ip_index: 0
    vrf: CORE
    description: ashcore2
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '1'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: GigabitEthernet2/0
    cidr: 10.224.23.8/31
    host_ip_index: 0
    vrf: TRUSTED
    description: ashcore2
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '2'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: GigabitEthernet2/1
    cidr: 10.224.23.10/31
    host_ip_index: 0
    vrf: TRUSTED
    description: ashfab1
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '2'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: Vlan10
    cidr: 10.224.13.24/29
    host_ip_index: 2
    vrf: CORE
    description: ashfw1
    enabled: true
    underlay: false
    physical: false
    ospf_active: false
    ospf_process: '0'
    bgp: false
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: false

  # --------
  # ashcore2
  # --------
  ashcore2:
  - name: Loopback0
    cidr: 10.224.3.4/32
    host_ip_index: 0
    vrf: GLOBAL
    description: main_loopback
    enabled: true
    underlay: false
    physical: false
    ospf_active: false
    ospf_process: 0
    bgp: false
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: no

  - name: Loopback1
    cidr: 10.224.113.4/32
    host_ip_index: 0
    vrf: CORE
    description: main_loopback
    enabled: true
    underlay: false
    physical: false
    ospf_active: true
    ospf_process: '1'
    bgp: false
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: false

  - name: Loopback2
    cidr: 10.224.123.4/32
    host_ip_index: 0
    vrf: TRUSTED
    description: main_loopback
    enabled: true
    underlay: false
    physical: false
    ospf_active: true
    ospf_process: '2'
    bgp: false
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: false

  - name: GigabitEthernet0/1
    cidr: 10.224.13.2/31
    host_ip_index: 1
    vrf: CORE
    description: ashwan1
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '1'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: GigabitEthernet1/1
    cidr: 10.224.23.2/31
    host_ip_index: 1
    vrf: TRUSTED
    description: ashwan1
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '2'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: GigabitEthernet0/2
    cidr: 10.224.13.6/31
    host_ip_index: 1
    vrf: CORE
    description: ashwan2
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '1'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: GigabitEthernet1/2
    cidr: 10.224.23.6/31
    host_ip_index: 1
    vrf: TRUSTED
    description: ashwan2
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '2'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: GigabitEthernet1/0
    cidr: 10.224.13.8/31
    host_ip_index: 1
    vrf: CORE
    description: ashcore1
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '1'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: GigabitEthernet2/0
    cidr: 10.224.23.8/31
    host_ip_index: 1
    vrf: TRUSTED
    description: ashcore1
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '2'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: GigabitEthernet2/2
    cidr: 10.224.23.12/31
    host_ip_index: 0
    vrf: TRUSTED
    description: ashfab2
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '2'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: true

  - name: Vlan10
    cidr: 10.224.13.24/29
    host_ip_index: 3
    vrf: CORE
    description: ashfw1
    enabled: true
    underlay: false
    physical: false
    ospf_active: false
    ospf_process: '0'
    bgp: false
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: false