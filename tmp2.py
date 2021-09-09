  - name: Build Interface-IP to BGP ASN mappings For Each Device
    set_fact:
      device_map: "{{ 
        device_map | default({}) |
        combine ({ (item.cidr | ipv4(item.host_ip_index) | ipaddr('address')) : item.bgp_local_as }) }}"
    loop: "{{ 
      l3_transit_loopback_interfaces[inventory_hostname] |
      selectattr('cidr', 'defined') |
      list }}"
    tags:
    - build_ip_asn_map
    - bgp_neighbor

  - name: Display the Dictionary
    debug: var=device_map
    tags:
    - build_ip_asn_map
    - bgp_neighbor

  - name: Combine Each Device Interface-IP to BGP ASN mappings 
    set_fact:
      ip_asn_map: "{{ ip_asn_map | default({}) | combine(item) }}"
    loop: "{{
          groups['all'] |
          map('extract', hostvars) |
          selectattr('device_map', 'defined') |
          map(attribute='device_map') |
          list }}"
    tags:
    - build_ip_asn_map
    - bgp_neighbor
