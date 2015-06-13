# Creating 2 independent loops using names for the nodes
#
# northwest --- north  --- northeast          alpha ---- beta ---- ceta --- delta -- golf -- whisky
#     |   \       |       /   |                 |                                              |
#     |    ----   |   ----    |                 |                                              |
#     |        \  |  /        |                 |                                              |
#    west ----  center ---   east               +----------------------------------------------+
#     |        /  |  \        |
#     |    ----   |   ----    |
#     |   /       |       \   |
# Southwest --- south  --- southeast

topo = { 'northwest' : ['north',     'west',      'center'],
         'north'     : ['northwest', 'northeast', 'center'],
         'northeast' : ['north',     'east',      'center'],
         'west'      : ['northwest', 'southwest', 'center'],
         'east'      : ['northeast', 'southeast', 'center'],
         'southwest' : ['south',     'west',      'center'],
         'south'     : ['southwest', 'southeast', 'center'],
         'southeast' : ['south',     'east',      'center'],
         'center'    : ['northwest', 'north', 'northeast',
                        'west',               'east',
                        'southwest', 'south', 'southeast'],
         'alpha'     : [ 'beta', 'whisky' ],
         'beta'      : [ 'alpha', 'ceta'  ],
         'ceta'      : [ 'beta',  'delta' ],
         'delta'     : [ 'ceta',  'golf'  ],
         'golf'      : [ 'delta', 'whisky'],
         'whisky'    : [ 'golf',  'alpha' ] }
