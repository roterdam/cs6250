# Topology with a single loop
# A --- B --- C
# |     |
# D --- E


topo = { 'A' : ['B', 'D'],
         'B' : ['A', 'C', 'E'],
         'C' : ['B'],
         'D' : ['A', 'E'],
         'E' : ['B', 'D'] }
