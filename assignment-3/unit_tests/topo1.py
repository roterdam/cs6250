# Topology is very simple:
# A --- B --- C

topo = { 'A' : ['B'], 
         'B' : ['A', 'C'],
         'C' : ['B'] }

ans = 'A:A0,B1,C2' + \
      'B:A1,B0,C1' + \
      'C:A2,B1,C0'