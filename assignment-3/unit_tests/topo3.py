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

ans = 'A:A0,B1,C2,D3,E2,F3,G4,H3,J4' + \
      'B:A1,B0,C1,D2,E1,F2,G3,H2,J3' + \
      'C:A2,B1,C0,D3,E2,F3,G4,H3,J4' + \
      'D:A3,B2,C3,D0,E1,F2,G1,H2,J3' + \
      'E:A2,B1,C2,D1,E0,F1,G2,H1,J2' + \
      'F:A3,B2,C3,D2,E1,F0,G3,H2,J1' + \
      'G:A4,B3,C4,D1,E2,F3,G0,H1,J2' + \
      'H:A3,B2,C3,D2,E1,F2,G1,H0,J1' + \
      'J:A4,B3,C4,D3,E2,F1,G2,H1,J0'