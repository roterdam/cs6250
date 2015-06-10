# Bad topology where C doesn't have a backlink to B. For testing purposes.
# A --- B --> C
# |     |
# D --- E


topo = { 'A' : ['B', 'D'],
         'B' : ['A', 'C', 'E'],
         'C' : [],
         'D' : ['A', 'E'],
         'E' : ['B', 'D'] }
