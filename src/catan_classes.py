import random

# (y,x) -> all points in code

# HELPER FUNCTIONS OVERALL
def dictionary_to_array(diction):
    arr = []
    for key in diction.keys():
        arr += [key for k in range(diction[key])]
    return arr

def array_to_dictionary(arr):
    diction = {}
    for item in arr:
        if item in diction.keys():
            diction[item] += 1
        else:
            diction[item] = 1
    return diction


# PLAYER BASED CLASSES
class Road:
    def __init__(self, color, points):
        self.color = color
        self.points = points
    
    def __eq__(self, value):
        return (self.color == value.color and ((self.points[0] == value.points[0] and self.points[1] == value.points[1]) or (self.points[1] == value.points[0] and self.points[0] == value.points[1])))

    def __repr__(self):
        return 'Road(color:' + self.color + ', points:[' + str(self.points[0]) + '->' + str(self.points[1]) + '])'


class House:
    def __init__(self, color, point, is_big_house=False):
        self.color = color
        self.point = point
        self.is_big_house = is_big_house
        self.victory_points = 1

    def multiplier(self):
        if self.is_big_house:
            return 2
        else:
            return 1
        
    def upgrade(self):
        self.is_big_house = True
        self.victory_points = 2

    def __eq__(self, value):
        if isinstance(value, House):
            return self.point == value.point and self.color == value.color
        else:
            return self.point == value
    
    def __repr__(self):
        return 'House(color:' + self.color + ', isBigHouse:' + str(self.is_big_house) + ', point:' + str(self.point) + ')'


class Robber:
    def __init__(self):
        self.point = (0, 0)

    def move(self, point):
        self.point = point


class Player:
    def __init__(self, color):
        self.color = color
        self.victory_points = 0
        self.wallet = {'Wood':0, 'Brick':0, 'Sheep':0, 'Wheat':0, 'Stone':0} # list of Resources
        self.trade_routes = ['4 to 1']

    def add_resources(self):
        return False
    
    def buy_road(self):  #Lucy made this <3
        # Cost = 1 Brick, 1 Wood                                                         
        if self.wallet['Wood'] > 0 and self.wallet['Brick'] > 0:        
            self.wallet['Wood'] -= 1
            self.wallet['Brick'] -= 1
            return True
        else:
            raise Exception('You Poor. Cry')
        
    def buy_house(self):
        # Cost = 1 Brick, 1 Wood, 1 Wheat, 1 Sheep
        if self.wallet['Wood'] > 0 and self.wallet['Brick'] > 0 and self.wallet['Wheat'] > 0 and self.wallet['Sheep'] > 0:
            self.wallet['Wood'] -= 1
            self.wallet['Brick'] -= 1
            self.wallet['Wheat'] -= 1
            self.wallet['Sheep'] -= 1
            return True
        else:
            raise Exception('You Poor. Cry')

    def check_for_trade_options(self, house):
        point = house.point
        if point == (0,3) or point == (1,2):
            self.trade_routes.append('3 to 1')
        if point == (5,10) or point == (6,10):
            self.trade_routes.append('3 to 1')
        if point == (11,5) or point == (10,6):
            self.trade_routes.append('3 to 1')
        if point == (11,3) or point == (10,2):
            self.trade_routes.append('3 to 1')
        if point == (3,1) or point == (4,1):
            self.trade_routes.append('2 Wood to 1')
        if point == (7,1) or point == (8,1):
            self.trade_routes.append('2 Brick to 1')
        if point == (8,9) or point == (9,8):
            self.trade_routes.append('2 Sheep to 1')
        if point == (0,5) or point == (1,6):
            self.trade_routes.append('2 Wheat to 1')
        if point == (2,8) or point == (3,9):
            self.trade_routes.append('2 Stone to 1')

    def upgrade_house(self):
        # Cost = 2 Wheat, 3 Stone
        if self.wallet['Wheat'] > 1 and self.wallet['Stone'] > 2:
            self.wallet['Wheat'] -= 2
            self.wallet['Stone'] -= 3
            return True
        else:
            raise Exception('You Poor. Cry')
    
    def trade_resource(self, dict_of_resources, returned_resource):
        # CHECK THEY HAVE THOSE RESOURCES
        for key in self.wallet.keys():
            if not self.wallet[key] >= dict_of_resources[key]:
                raise Exception('You don\'t have those resources.')
        
        array_of_resources = dictionary_to_array(dict_of_resources)
            
        # CHECK THEIR TRADE OPTIONS
        if '2 Wood to 1' in self.trade_routes:
            if dict_of_resources['Wood'] > 1:
                self.wallet['Wood'] -= 2
                self.wallet[returned_resource] += 1

        elif '2 Brick to 1' in self.trade_routes:
            if dict_of_resources['Brick'] > 1:
                self.wallet['Brick'] -= 2
                self.wallet[returned_resource] += 1

        elif '2 Sheep to 1' in self.trade_routes:
            if dict_of_resources['Sheep'] > 1:
                self.wallet['Sheep'] -= 2
                self.wallet[returned_resource] += 1

        elif '2 Wheat to 1' in self.trade_routes:
            if dict_of_resources['Wheat'] > 1:
                self.wallet['Wheat'] -= 2
                self.wallet[returned_resource] += 1

        elif '2 Stone to 1' in self.trade_routes:
            if dict_of_resources['Stone'] > 1:
                self.wallet['Stone'] -= 2
                self.wallet[returned_resource] += 1

        elif '3 to 1' in self.trade_routes:
            if len(array_of_resources) > 2:
                spent_resources = array_of_resources[0:3]
                dict_of_spent = array_to_dictionary(spent_resources)
                for key in dict_of_spent.keys():
                    self.wallet[key] -= dict_of_spent[key]
                
        elif '4 to 1' in self.trade_routes:
            if len(array_of_resources) > 3:
                spent_resources = array_of_resources[0:4]
                dict_of_spent = array_to_dictionary(spent_resources)
                for key in dict_of_spent.keys():
                    self.wallet[key] -= dict_of_spent[key]

        raise Exception('No possible trades.')
    

# BOARD BASED CLASSES
class Resource_Hex:
    def __init__(self, points, resource, dice_score):
        self.points = points
        self.resource = resource
        self.dice_score = dice_score

    def __repr__(self):
        return 'Hex(resource:' + self.resource  + ', dice:' +  str(self.dice_score) + ', points:' + str(self.points) + ')'
    

class Board: 
    def get_numerical_board(self):
        numerical_board = [
        [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0]
        ]
        return numerical_board
    
    def get_hexagon_combinations(self):
        all_combinations = [
            [(0,3),(1,4),(2,4),(3,3),(2,2),(1,2)],
            [(0,5),(1,6),(2,6),(3,5),(2,4),(1,4)],
            [(0,7),(1,8),(2,8),(3,7),(2,6),(1,6)],
            [(2,2),(3,3),(4,3),(5,2),(4,1),(3,1)],
            [(2,4),(3,5),(4,5),(5,4),(4,3),(3,3)],
            [(2,6),(3,7),(4,7),(5,6),(4,5),(3,5)],
            [(2,8),(3,9),(4,9),(5,8),(4,7),(3,7)],
            [(4,1),(5,2),(6,2),(7,1),(6,0),(5,0)],
            [(4,3),(5,4),(6,4),(7,3),(6,2),(5,2)],
            [(4,5),(5,6),(6,6),(7,5),(6,4),(5,4)],
            [(4,7),(5,8),(6,8),(7,7),(6,6),(5,6)],
            [(4,9),(5,10),(6,10),(7,9),(6,8),(5,8)],
            [(6,2),(7,3),(8,3),(9,2),(8,1),(7,1)],
            [(6,4),(7,5),(8,5),(9,4),(8,3),(7,3)],
            [(6,6),(7,7),(8,7),(9,6),(8,5),(7,5)],
            [(6,8),(7,9),(8,9),(9,8),(8,7),(7,7)],
            [(8,3),(9,4),(10,4),(11,3),(10,2),(9,2)],
            [(8,5),(9,6),(10,6),(11,5),(10,4),(9,4)],
            [(8,7),(9,8),(10,8),(11,7),(10,6),(9,6)]
        ]
        return all_combinations

    def random_resource(self, dict_of_resources):
        resource_names = dict_of_resources.keys()
        rand_resource_key = resource_names[random.randint(0, len(dict_of_resources) - 1)]

        dict_of_resources[rand_resource_key] -= 1
        if dict_of_resources[rand_resource_key] == 0:
            del dict_of_resources[rand_resource_key]
        return rand_resource_key, dict_of_resources

    def randomize_hexes(self):
        resource_types = {'Wood':4, 'Brick':3, 'Sheep':4, 'Wheat':4, 'Stone':3, 'Desert':1}
        dice_list = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        point_combinations = self.get_hexagon_combinations()
        list_of_hexes = []
        for i in range(19): # standard size of board
            points = point_combinations[i]
            resource, resource_types = self.random_resource(resource_types)
            dice_score = 0
            if resource == 'Desert':
                dice_score = 0
            else:
                random_score = random.randint(0, len(dice_list) - 1)
                dice_score = dice_list[random_score]
                dice_list.pop(random_score)
            resource_hex = Resource_Hex(points=points, resource=resource, dice_score=dice_score)
            list_of_hexes.append(resource_hex)

        return list_of_hexes

    def __init__(self):
        self.hexes = self.randomize_hexes()
    

class Catan:
    def num_to_color(self, player_count):
        colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'white', 'black']
        return colors[player_count]
    
    def neighbor_points(self, point):
        neighbors = []
        for i in range(3):
            for j in range(3):
                neighbor = (point[0] - 1 + i, point[1] - 1 + j)
                neighbors.append(neighbor)
                if (neighbor[0] < 0 or neighbor[0] > 11 or neighbor[1] < 0 or neighbor[1] > 10):
                    neighbors.pop()
                if neighbor == point:
                    neighbors.pop()
        return neighbors
    
    def check_in_eight(self, point1, point2):
        #board_size x = 0:10, y = 0:11
        y = point1[0]
        x = point1[1]
        nearby_points = []

        # corners
        if x == 0 and y == 0:
            nearby_points = [(y+1, x), (y+1, x+1), (y, x+1)]
        elif x == 0 and y == 11:
            nearby_points = [(y+1, x), (y+1, x-1), (y, x-1)]
        elif x == 10 and y == 0:
            nearby_points = [(y-1, y), (y-1, x+1), (y, y+1)]
        elif x == 10 and y == 11:
            nearby_points = [(y-1, y), (y-1, x-1), (y, y-1)]
        # sides
        elif x == 0:
            nearby_points = [(y, x-1), (y, x+1), (y+1, x-1), (y+1, x), (y+1, x+1)]
        elif x == 10:
            nearby_points = [(y, x-1), (y, x+1), (y-1, x-1), (y-1, x), (y-1, x+1)]
        elif y == 0:
            nearby_points = [(y-1, x), (y+1, x), (y-1, x+1), (y, x+1), (y+1, x+1)]
        elif y == 11:
            nearby_points = [(y-1, x), (y+1, x), (y-1, x-1), (y, x-1), (y+1, x-1)]
        # middle
        else:
            nearby_points = [(y-1, x-1), (y-1, x), (y-1, x+1), (y, x-1), (y, x+1), (y+1, x-1), (y+1, x), (y+1, x+1)]

        return (point2 in nearby_points)
    
    def check_houses_for_roads(self, point, color):
        houses = self.houses
        for house in houses:
            if point == house.point:
                if not (color == house.color):
                    return False
        return True

    def __init__(self, player_count):
        self.players = {self.num_to_color(k):Player(self.num_to_color(k)) for k in range(player_count)}
        self.board = Board()
        self.roads = []
        self.houses = []

    def check_availability(self, obj):
        if isinstance(obj, Road):
            # CHECK ROAD ISN'T TAKEN
            for road in self.roads:
                if road.points == obj.points:
                    raise Exception('Road space is taken.') # Road space is taken
                
            # CHECK ROAD IS A VALID SETUP
            valid_board = self.board.get_numerical_board()
            point1 = obj.points[0]
            point2 = obj.points[1]
            if valid_board[point1[0]][point1[1]] == 1:
                if valid_board[point2[0]][point2[1]] == 1:
                    if not (point2 in self.neighbor_points(point1)):
                        raise Exception('Points aren\'t near each other.') # Points aren't near each other
                else:
                    raise Exception('Second Point isn\'t valid.') # Second Point isn't valid
            else:
                raise Exception('First Point isn\'t valid.') # First Point isn't valid
            
            # CHECK ROAD IS PLAYER ALLOWED
            for road in self.get_player_roads(obj.color):
                player_road_p1 = road.points[0]
                player_road_p2 = road.points[1]
                obj_road_p1 = obj.points[0]
                obj_road_p2 = obj.points[1]

                if player_road_p1 == obj_road_p1:
                    important_point = obj_road_p1
                    if (self.check_houses_for_roads(important_point, obj.color)):
                        return True
                elif player_road_p1 == obj_road_p2:
                    important_point = obj_road_p2
                    if (self.check_houses_for_roads(important_point, obj.color)):
                        return True
                elif player_road_p2 == obj_road_p1:
                    important_point = obj_road_p1
                    if (self.check_houses_for_roads(important_point, obj.color)):
                        return True
                elif player_road_p2 == obj_road_p2:
                    important_point = obj_road_p2
                    if (self.check_houses_for_roads(important_point, obj.color)):
                        return True
            raise Exception('You don\'t have a connecting road.')
       
       
        elif isinstance(obj, House):
            # CHECK HOUSE ISN'T TAKEN
            for house in self.houses:
                if house.point == obj.point:
                    raise Exception('House spot is taken.')
                
            # CHECK HOUSE IS VALID SPOT
            valid_board = self.board.get_numerical_board()
            if not valid_board[obj.point[0]][obj.point[1]] == 1:
                raise Exception('House is off board.')
            
            # CHECK HOUSE IS NOT NEXT TO ANOTHER HOUSE
            neighbors = self.neighbor_points(obj.point)
            for house in self.houses:
                if house.point in neighbors:
                    raise Exception('House is too close to another.')

            # CHECK HOUSE IS PLAYER ALLOWED
            player_roads = self.get_player_roads(obj.color)
            for player_road in player_roads:
                if obj.point == player_road.points[0] or obj.point == player_road.points[1]:
                    return True
            raise Exception('No valid Road connection.')
        else:
            return Exception('Not a road or house?')
        
    def get_player_roads(self, color):
        player_roads = []
        for road in self.roads:
            if road.color == color:
                player_roads.append(road)
        return player_roads
    
    def get_player_houses(self, color):
        player_houses = []
        for house in self.houses:
            if house.color == color:
                player_houses.append(house)
        return player_houses
        
    def player_buys_road(self, color, road):
        player = self.players[color]
        try:
            if color == road.color:
                if self.check_availability(road):
                    if player.buy_road():
                        self.roads.append(road)
                        print('bought road')
            else:
                raise Exception('YOURE THE WRONG PERSON')
        except Exception as e:
            print(e)

    def player_buys_house(self, color, house):
        player = self.players[color]
        try:
            if color == house.color:
                if self.check_availability(house):
                    if player.buy_house():
                        player.check_for_trade_options(house)
                        self.houses.append(house)
                        print('bought house')
            else:
                raise Exception('YOURE THE WRONG PERSON')
        except Exception as e:
            print(e)

    def player_upgrade_house(self, color, house):
        player = self.players[color]
        try:
            if color == house.color:
                if house in self.houses:
                    index_of_house = self.houses.index(house)
                    if player.upgrade_house():
                        self.houses.pop(index_of_house)
                        self.houses.append(house)
                        print('upgraded house')
                else:
                    raise Exception('That house doesn\'t exist.')
            else:
                raise Exception('YOURE THE WRONG PERSON')
        except Exception as e:
            print(e)

    def player_trade_resource(self, color, trade_resources, returned_resource):
        player = self.players[color]
        try:
            player.trade_resource(trade_resources, returned_resource)
        except Exception as e:
            print(e)