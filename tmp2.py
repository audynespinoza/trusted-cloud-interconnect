  # -------
  # mckwan1
  # -------
  mckwan1:
  - name: Loopback0
    cidr: 10.224.2.1/32
    host_ip_index: 0
    vrf: GLOBAL
    description: main_loopback
    enabled: true
    underlay: false
    physical: false
    ospf_active: true
    ospf_process: 0
    bgp: false
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: no

  - name: Loopback1
    cidr: 10.224.112.1/32
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
    bgp_route_reflect: no
    
  - name: Loopback2
    cidr: 10.224.122.1/32
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
    bgp_route_reflect: no
    
  - name: GigabitEthernet0/1
    cidr: 10.224.12.0/31
    host_ip_index: 0
    vrf: CORE
    description: mckcore1
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '1'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: true
    bgp_route_reflect: no
    
  - name: GigabitEthernet0/3
    cidr: 10.224.22.0/31
    host_ip_index: 0
    vrf: TRUSTED
    description: mckcore1
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '2'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: true
    bgp_route_reflect: no
    
  - name: GigabitEthernet0/2
    cidr: 10.224.12.2/31
    host_ip_index: 0
    vrf: CORE
    description: mckcore2
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '1'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: true
    bgp_route_reflect: no
    
  - name: GigabitEthernet0/4
    cidr: 10.224.22.2/31
    host_ip_index: 0
    vrf: TRUSTED
    description: mckcore2
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '2'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: true
    bgp_route_reflect: no
    
  - name: GigabitEthernet0/5
    cidr: 10.224.253.4/31
    host_ip_index: 0
    vrf: EDGE
    description: ashwan1
    enabled: true
    underlay: true
    physical: true
    ospf_active: false
    ospf_process: '0'
    bgp: false
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: no
    
  - name: Tunnel1
    cidr: 10.224.254.4/31
    host_ip_index: 0
    vrf: CORE
    description: ashwan1
    enabled: true
    underlay: false
    physical: false
    ospf_active: false
    ospf_process: '0'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: no
    tunnel_source: GigabitEthernet0/5
    tunnel_destination: 10.224.253.5
    
  - name: Tunnel2
    cidr: 10.224.255.4/31 
    host_ip_index: 0
    vrf: TRUSTED
    description: ashwan1
    enabled: true
    underlay: false
    physical: false
    ospf_active: false
    ospf_process: '0'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: no
    tunnel_source: GigabitEthernet0/5
    tunnel_destination: 10.224.253.5

  # -------
  # mckwan2
  # -------
  mckwan2:
  - name: Loopback0
    cidr: 10.224.2.2/32
    host_ip_index: 0
    vrf: GLOBAL
    description: main_loopback
    enabled: true
    underlay: false
    physical: false
    ospf_active: true
    ospf_process: 0
    bgp: false
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: no

  - name: Loopback1
    cidr: 10.224.112.2/32
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
    bgp_route_reflect: no
    
  - name: Loopback2
    cidr: 10.224.122.2/32
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
    bgp_route_reflect: no
    
  - name: GigabitEthernet0/1
    cidr: 10.224.12.4/31
    host_ip_index: 0
    vrf: CORE
    description: mckcore1
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '1'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: true
    bgp_route_reflect: no
    
  - name: GigabitEthernet0/2
    cidr: 10.224.12.6/31
    host_ip_index: 0
    vrf: CORE
    description: mckcore2
    enabled: true
    underlay: false
    physical: true
    ospf_active: true
    ospf_process: '1'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: true
    bgp_route_reflect: no
    
  - name: GigabitEthernet0/3
    cidr: 10.224.253.6/31
    host_ip_index: 0
    vrf: EDGE
    description: ashwan3
    enabled: true
    underlay: true
    physical: true
    ospf_active: false
    ospf_process: '0'
    bgp: false
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: no
    
  - name: Tunnel1
    cidr: 10.224.254.6/31
    host_ip_index: 0
    vrf: CORE
    description: ashwan3
    enabled: true
    underlay: false
    physical: false
    ospf_active: false
    ospf_process: '0'
    bgp: true
    bgp_local_as: "{{ bgp.local_as }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: no
    tunnel_source: GigabitEthernet0/3
    tunnel_destination: 10.224.253.7
