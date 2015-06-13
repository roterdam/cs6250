# More interesting topology
# A --- B --- C
#       |
# D --- E --- F
# |     |     |
# G --- H --- J

topo = { 'A' : ['B'],
         'B' : ['A', 'C', 'E'],
         'C' : ['B'],
         'D' : ['E', 'G'],
         'E' : ['B', 'D', 'F', 'H'],
         'F' : ['E', 'J'],
         'G' : ['D', 'H'],
         'H' : ['E', 'G', 'J'],
         'J' : ['F', 'H'] }
