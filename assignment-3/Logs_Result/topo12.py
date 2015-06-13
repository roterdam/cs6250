# Topology is very simple:
# A --- B --- C
# D --- E --- F
topo = { 'A' : ['B'],
         'B' : ['A', 'C'],
         'C' : ['B'],
         'D' : ['E'], 
         'E' : ['D', 'F'],
         'F' : ['E'] }
