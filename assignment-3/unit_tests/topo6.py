# a Star topology centered on Z with a loop around the outside
# +-------------D---------G---------J------------+
# |              \        |        /             |
# |               \       |       /              |
# |                E      H      K               |
# |                 \     |     /                |
# |                  \    |    /                 |
# |                   F   I   L                  |
# |                    \  |  /                   |
# |                     \ | /                    |
# A --- B --- C --------- Z -------- M --- N --- O
# |                     / | \                    |
# |                    /  |  \                   |
# |                   P   S   V                  |
# |                  /    |    \                 |
# |                 /     |     \                |
# |                Q      T      W               |
# |               /       |       \              |
# |              /        |        \             |
# +-------------R---------U---------X------------+

topo = { 'A' : ['B', 'D', 'R'],
         'B' : ['A', 'C'],
         'C' : ['B', 'Z'],
         'D' : ['A', 'E', 'G'],
         'E' : ['D', 'F'],
         'F' : ['E', 'Z'],
         'G' : ['D', 'H', 'J'],
         'H' : ['G', 'I'],
         'I' : ['H', 'Z'],
         'J' : ['G', 'K', 'O'],
         'K' : ['J', 'L'],
         'L' : ['K', 'Z'],
         'M' : ['Z', 'N'],
         'N' : ['M', 'O'],
         'O' : ['J', 'N', 'X'],
         'P' : ['Z', 'Q'],
         'Q' : ['P', 'R'],
         'R' : ['A', 'Q', 'U'],
         'S' : ['Z', 'T'],
         'T' : ['S', 'U'],
         'U' : ['R', 'T', 'X'],
         'V' : ['Z', 'W'],
         'W' : ['V', 'X'],
         'X' : ['U', 'W', 'O'],
         'Z' : ['C', 'F', 'I', 'L', 'M', 'P', 'S', 'V']}

ans = \
'A:A0,B1,C2,D1,E2,F3,G2,H3,I4,J3,K4,L4,M4,N5,O4,P3,Q2,R1,S4,T3,U2,V4,W4,X3,Z3' + \
'B:A1,B0,C1,D2,E3,F3,G3,H4,I3,J4,K4,L3,M3,N4,O5,P3,Q3,R2,S3,T4,U3,V3,W4,X4,Z2' + \
'C:A2,B1,C0,D3,E3,F2,G4,H3,I2,J4,K3,L2,M2,N3,O4,P2,Q3,R3,S2,T3,U4,V2,W3,X4,Z1' + \
'D:A1,B2,C3,D0,E1,F2,G1,H2,I3,J2,K3,L4,M4,N4,O3,P4,Q3,R2,S4,T4,U3,V4,W5,X4,Z3' + \
'E:A2,B3,C3,D1,E0,F1,G2,H3,I3,J3,K4,L3,M3,N4,O4,P3,Q4,R3,S3,T4,U4,V3,W4,X5,Z2' + \
'F:A3,B3,C2,D2,E1,F0,G3,H3,I2,J4,K3,L2,M2,N3,O4,P2,Q3,R4,S2,T3,U4,V2,W3,X4,Z1' + \
'G:A2,B3,C4,D1,E2,F3,G0,H1,I2,J1,K2,L3,M4,N3,O2,P4,Q4,R3,S4,T5,U4,V4,W4,X3,Z3' + \
'H:A3,B4,C3,D2,E3,F3,G1,H0,I1,J2,K3,L3,M3,N4,O3,P3,Q4,R4,S3,T4,U5,V3,W4,X4,Z2' + \
'I:A4,B3,C2,D3,E3,F2,G2,H1,I0,J3,K3,L2,M2,N3,O4,P2,Q3,R4,S2,T3,U4,V2,W3,X4,Z1' + \
'J:A3,B4,C4,D2,E3,F4,G1,H2,I3,J0,K1,L2,M3,N2,O1,P4,Q5,R4,S4,T4,U3,V4,W3,X2,Z3' + \
'K:A4,B4,C3,D3,E4,F3,G2,H3,I3,J1,K0,L1,M3,N3,O2,P3,Q4,R5,S3,T4,U4,V3,W4,X3,Z2' + \
'L:A4,B3,C2,D4,E3,F2,G3,H3,I2,J2,K1,L0,M2,N3,O3,P2,Q3,R4,S2,T3,U4,V2,W3,X4,Z1' + \
'M:A4,B3,C2,D4,E3,F2,G4,H3,I2,J3,K3,L2,M0,N1,O2,P2,Q3,R4,S2,T3,U4,V2,W3,X3,Z1' + \
'N:A5,B4,C3,D4,E4,F3,G3,H4,I3,J2,K3,L3,M1,N0,O1,P3,Q4,R4,S3,T4,U3,V3,W3,X2,Z2' + \
'O:A4,B5,C4,D3,E4,F4,G2,H3,I4,J1,K2,L3,M2,N1,O0,P4,Q4,R3,S4,T3,U2,V3,W2,X1,Z3' + \
'P:A3,B3,C2,D4,E3,F2,G4,H3,I2,J4,K3,L2,M2,N3,O4,P0,Q1,R2,S2,T3,U3,V2,W3,X4,Z1' + \
'Q:A2,B3,C3,D3,E4,F3,G4,H4,I3,J5,K4,L3,M3,N4,O4,P1,Q0,R1,S3,T3,U2,V3,W4,X3,Z2' + \
'R:A1,B2,C3,D2,E3,F4,G3,H4,I4,J4,K5,L4,M4,N4,O3,P2,Q1,R0,S3,T2,U1,V4,W3,X2,Z3' + \
'S:A4,B3,C2,D4,E3,F2,G4,H3,I2,J4,K3,L2,M2,N3,O4,P2,Q3,R3,S0,T1,U2,V2,W3,X3,Z1' + \
'T:A3,B4,C3,D4,E4,F3,G5,H4,I3,J4,K4,L3,M3,N4,O3,P3,Q3,R2,S1,T0,U1,V3,W3,X2,Z2' + \
'U:A2,B3,C4,D3,E4,F4,G4,H5,I4,J3,K4,L4,M4,N3,O2,P3,Q2,R1,S2,T1,U0,V3,W2,X1,Z3' + \
'V:A4,B3,C2,D4,E3,F2,G4,H3,I2,J4,K3,L2,M2,N3,O3,P2,Q3,R4,S2,T3,U3,V0,W1,X2,Z1' + \
'W:A4,B4,C3,D5,E4,F3,G4,H4,I3,J3,K4,L3,M3,N3,O2,P3,Q4,R3,S3,T3,U2,V1,W0,X1,Z2' + \
'X:A3,B4,C4,D4,E5,F4,G3,H4,I4,J2,K3,L4,M3,N2,O1,P4,Q3,R2,S3,T2,U1,V2,W1,X0,Z3' + \
'Z:A3,B2,C1,D3,E2,F1,G3,H2,I1,J3,K2,L1,M1,N2,O3,P1,Q2,R3,S1,T2,U3,V1,W2,X3,Z0'