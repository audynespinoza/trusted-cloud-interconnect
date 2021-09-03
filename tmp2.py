l3_interfaces:
  ashwan2:
  - name: Loopback1
    cidr: 10.224.113.2/32
    host_ip_index: 0
    vrf: CORE
    description: main_loopback
    enabled: true
    underlay: false
    physical: false
    ospf_active: true
    ospf_process: '1'
    bgp: false
    bgp_type: false
    bgp_local_as: "{{ bgp.local_asn }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: false
    
  - name: Loopback2
    cidr: 10.224.123.2/32
    host_ip_index: 0
    vrf: TRUSTED
    description: main_loopback
    enabled: true
    underlay: false
    physical: false
    ospf_active: true
    ospf_process: '2'
    bgp: false
    bgp_type: false
    bgp_local_as: "{{ bgp.local_asn }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: false
    


    

  - name: GigabitEthernet0/5
    cidr: 10.224.253.0/31
    host_ip_index: 0
    vrf: EDGE
    description: alnwan1
    enabled: true
    underlay: true
    physical: true
    ospf_active: false
    ospf_process: '0'
    bgp: false
    bgp_type: false
    bgp_local_as: "{{ bgp.local_asn }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: false
    
  - name: Tunnel1
    cidr: 10.224.254.0/31
    host_ip_index: 1
    vrf: CORE
    description: alnwan1
    enabled: true
    underlay: false
    physical: false
    ospf_active: false
    ospf_process: '0'
    bgp: true
    bgp_type: external
    bgp_local_as: "{{ bgp.local_asn }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: false
    
  - name: Tunnel2
    cidr: 10.224.255.0/31 
    host_ip_index: 1
    vrf: TRUSTED
    description: alnwan4
    enabled: true
    underlay: false
    physical: false
    ospf_active: false
    ospf_process: '0'
    bgp: true
    bgp_type: external
    bgp_local_as: "{{ bgp.local_asn }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: false
    
  ashwan4:
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
    bgp_type: false
    bgp_local_as: "{{ bgp.local_asn }}"
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
    bgp_type: false
    bgp_local_as: "{{ bgp.local_asn }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: false
    

  - name: GigabitEthernet0/3
    cidr: 10.224.253.2/31
    host_ip_index: 1
    vrf: EDGE
    description: alnwan2
    enabled: true
    underlay: true
    physical: true
    ospf_active: false
    ospf_process: '0'
    bgp: false
    bgp_type: false
    bgp_local_as: "{{ bgp.local_asn }}"
    bgp_enabled: false
    bgp_next_hop_self: false
    bgp_route_reflect: false
    
  - name: Tunnel1
    cidr: 10.224.254.2/31
    host_ip_index: 1
    vrf: CORE
    description: alnwan2
    enabled: true
    underlay: false
    physical: false
    ospf_active: false
    ospf_process: '0'
    bgp: true
    bgp_type: external
    bgp_local_as: "{{ bgp.local_asn }}"
    bgp_enabled: true
    bgp_next_hop_self: false
    bgp_route_reflect: false

