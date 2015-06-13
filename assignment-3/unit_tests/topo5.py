# a Star topology centered on Z
#               D         G         J
#                \        |        /
#                 \       |       /
#                  E      H      K
#                   \     |     /
#                    \    |    /
#                     F   I   L
#                      \  |  /
#                       \ | /
# A --- B --- C --------- Z -------- M --- N --- O
#                       / | \
#                      /  |  \
#                     P   S   V
#                    /    |    \
#                   /     |     \
#                  Q      T      W
#                 /       |       \
#                /        |        \
#               R         U         X
#
topo = { 'A' : ['B'],
         'B' : ['A', 'C'],
         'C' : ['B', 'Z'],
         'D' : ['E'],
         'E' : ['D', 'F'],
         'F' : ['E', 'Z'],
         'G' : ['H'],
         'H' : ['G', 'I'],
         'I' : ['H', 'Z'],
         'J' : ['K'],
         'K' : ['J', 'L'],
         'L' : ['K', 'Z'],
         'M' : ['Z', 'N'],
         'N' : ['M', 'O'],
         'O' : ['N'],
         'P' : ['Z', 'Q'],
         'Q' : ['P', 'R'],
         'R' : ['Q'],
         'S' : ['Z', 'T'],
         'T' : ['S', 'U'],
         'U' : ['T'],
         'V' : ['Z', 'W'],
         'W' : ['V', 'X'],
         'X' : ['W'],
         'Z' : ['C', 'F', 'I', 'L', 'M', 'P', 'S', 'V']}

ans = \
'A:A0,B1,C2,D6,E5,F4,G6,H5,I4,J6,K5,L4,M4,N5,O6,P4,Q5,R6,S4,T5,U6,V4,W5,X6,Z3' + \
'B:A1,B0,C1,D5,E4,F3,G5,H4,I3,J5,K4,L3,M3,N4,O5,P3,Q4,R5,S3,T4,U5,V3,W4,X5,Z2' + \
'C:A2,B1,C0,D4,E3,F2,G4,H3,I2,J4,K3,L2,M2,N3,O4,P2,Q3,R4,S2,T3,U4,V2,W3,X4,Z1' + \
'D:A6,B5,C4,D0,E1,F2,G6,H5,I4,J6,K5,L4,M4,N5,O6,P4,Q5,R6,S4,T5,U6,V4,W5,X6,Z3' + \
'E:A5,B4,C3,D1,E0,F1,G5,H4,I3,J5,K4,L3,M3,N4,O5,P3,Q4,R5,S3,T4,U5,V3,W4,X5,Z2' + \
'F:A4,B3,C2,D2,E1,F0,G4,H3,I2,J4,K3,L2,M2,N3,O4,P2,Q3,R4,S2,T3,U4,V2,W3,X4,Z1' + \
'G:A6,B5,C4,D6,E5,F4,G0,H1,I2,J6,K5,L4,M4,N5,O6,P4,Q5,R6,S4,T5,U6,V4,W5,X6,Z3' + \
'H:A5,B4,C3,D5,E4,F3,G1,H0,I1,J5,K4,L3,M3,N4,O5,P3,Q4,R5,S3,T4,U5,V3,W4,X5,Z2' + \
'I:A4,B3,C2,D4,E3,F2,G2,H1,I0,J4,K3,L2,M2,N3,O4,P2,Q3,R4,S2,T3,U4,V2,W3,X4,Z1' + \
'J:A6,B5,C4,D6,E5,F4,G6,H5,I4,J0,K1,L2,M4,N5,O6,P4,Q5,R6,S4,T5,U6,V4,W5,X6,Z3' + \
'K:A5,B4,C3,D5,E4,F3,G5,H4,I3,J1,K0,L1,M3,N4,O5,P3,Q4,R5,S3,T4,U5,V3,W4,X5,Z2' + \
'L:A4,B3,C2,D4,E3,F2,G4,H3,I2,J2,K1,L0,M2,N3,O4,P2,Q3,R4,S2,T3,U4,V2,W3,X4,Z1' + \
'M:A4,B3,C2,D4,E3,F2,G4,H3,I2,J4,K3,L2,M0,N1,O2,P2,Q3,R4,S2,T3,U4,V2,W3,X4,Z1' + \
'N:A5,B4,C3,D5,E4,F3,G5,H4,I3,J5,K4,L3,M1,N0,O1,P3,Q4,R5,S3,T4,U5,V3,W4,X5,Z2' + \
'O:A6,B5,C4,D6,E5,F4,G6,H5,I4,J6,K5,L4,M2,N1,O0,P4,Q5,R6,S4,T5,U6,V4,W5,X6,Z3' + \
'P:A4,B3,C2,D4,E3,F2,G4,H3,I2,J4,K3,L2,M2,N3,O4,P0,Q1,R2,S2,T3,U4,V2,W3,X4,Z1' + \
'Q:A5,B4,C3,D5,E4,F3,G5,H4,I3,J5,K4,L3,M3,N4,O5,P1,Q0,R1,S3,T4,U5,V3,W4,X5,Z2' + \
'R:A6,B5,C4,D6,E5,F4,G6,H5,I4,J6,K5,L4,M4,N5,O6,P2,Q1,R0,S4,T5,U6,V4,W5,X6,Z3' + \
'S:A4,B3,C2,D4,E3,F2,G4,H3,I2,J4,K3,L2,M2,N3,O4,P2,Q3,R4,S0,T1,U2,V2,W3,X4,Z1' + \
'T:A5,B4,C3,D5,E4,F3,G5,H4,I3,J5,K4,L3,M3,N4,O5,P3,Q4,R5,S1,T0,U1,V3,W4,X5,Z2' + \
'U:A6,B5,C4,D6,E5,F4,G6,H5,I4,J6,K5,L4,M4,N5,O6,P4,Q5,R6,S2,T1,U0,V4,W5,X6,Z3' + \
'V:A4,B3,C2,D4,E3,F2,G4,H3,I2,J4,K3,L2,M2,N3,O4,P2,Q3,R4,S2,T3,U4,V0,W1,X2,Z1' + \
'W:A5,B4,C3,D5,E4,F3,G5,H4,I3,J5,K4,L3,M3,N4,O5,P3,Q4,R5,S3,T4,U5,V1,W0,X1,Z2' + \
'X:A6,B5,C4,D6,E5,F4,G6,H5,I4,J6,K5,L4,M4,N5,O6,P4,Q5,R6,S4,T5,U6,V2,W1,X0,Z3' + \
'Z:A3,B2,C1,D3,E2,F1,G3,H2,I1,J3,K2,L1,M1,N2,O3,P1,Q2,R3,S1,T2,U3,V1,W2,X3,Z0'