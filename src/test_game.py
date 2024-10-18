from catan_classes import *

catan = Catan(2)
catan.roads.append(Road('blue', [(0,3),(1,4)]))
catan.roads.append(Road('red', [(3,1),(4,1)]))
catan.players['blue'].wallet['Wood'] = 2
catan.players['blue'].wallet['Brick'] = 2
road = Road('blue', [(2,4),(1,4)])
catan.player_buys_road('blue', road)

catan.players['blue'].wallet['Wheat'] = 1
catan.players['blue'].wallet['Sheep'] = 1
house = House('blue', (1,4))
catan.player_buys_house('blue', house)

catan.players['blue'].wallet['Wheat'] = 2
catan.players['blue'].wallet['Stone'] = 3

house2 = House('blue', (1,4), True)
catan.player_upgrade_house('blue', house2)


