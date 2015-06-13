# multi loop topology
#  --ABB--ABC        BBA--BBB--
# |   |    |          |    |   |
# |  ABA--AB--AC  BA--BB--BBC  |
# |  |     |   |  |   |     |  |
#  --|-    AA--A--B--BC    -|--
#    | |       |  |       | |
#  --  |   DC--D--C--CA   |  --
# |    |   |   |  |   |   |    |
# |  DBC--DB--DA  CC--CB--CBA  |
# |   |    |          |    |   |
#  --DBB--DBA        CBC--CBB--



topo = {'A' : ['B', 'D', 'AA', 'AC'],
        'B' : ['A', 'C', 'BA', 'BC'],
        'C' : ['B', 'D', 'CA', 'CC'],
        'D' : ['A', 'C', 'DA', 'DC'],
        'AA' : ['A', 'AB'],
        'AB' : ['AA', 'AC', 'ABA', 'ABC'],
        'AC' : ['A', 'AB'],
        'ABA' : ['AB', 'ABB', 'DBB'],
        'ABB' : ['ABA', 'ABC', 'DBC'],
        'ABC' : ['AB', 'ABB'],
        'BA' : ['B', 'BB'],
        'BB' : ['BA', 'BC', 'BBA', 'BBC'],
        'BC' : ['B', 'BB'],
        'BBA' : ['BB', 'BBB'],
        'BBB' : ['BBA', 'BBC', 'CBA'],
        'BBC' : ['BB', 'BBB', 'CBB'],
        'CA' : ['C', 'CB'],
        'CB' : ['CA', 'CC', 'CBA', 'CBC'],
        'CC' : ['C', 'CB'],
        'CBA' : ['CB', 'CBB', 'BBB'],
        'CBB' : ['CBA', 'CBC', 'BBC'],
        'CBC' : ['CB', 'CBB'],
        'DA' : ['D', 'DB'],
        'DB' : ['DA', 'DC', 'DBA', 'DBC'],
        'DC' : ['D', 'DB'],
        'DBA' : ['DB', 'DBB'],
        'DBB' : ['DBA', 'DBC', 'ABA'],
        'DBC' : ['DB', 'DBB', 'ABB'] }
