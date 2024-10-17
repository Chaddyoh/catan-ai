import random

# (y,x) -> all points in code

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
    def __init__(self, color, point):
        self.color = color
        self.point = point
        self.is_big_house = False
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
        return self.color == value.color and self.point == value.point
    
    def __repr__(self):
        return 'House(color' + self.color + ', point:' + str(self.point) + ')'


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
        self.roads = [] # list of Roads
        self.houses = [] # list of Houses

    def add_resources(self):
        return False
    
    def buy_road(self, is_placable, points):  #Lucy made this <3
        # Cost = 1 Brick, 1 Wood   
        if is_placable:                                                         
            if self.wallet['Wood'] > 0 and self.wallet['Brick'] > 0:        
                self.wallet['Wood'] -= 1
                self.wallet['Brick'] -= 1
                self.roads.append(Road(self.color, points))
                return True
            else:
                raise Exception('You Poor. Cry')
        raise Exception('Something went wrong when purchasing.')
        
    def buy_house(self):
        return False

    def upgrade_house(self, point):
        return False
    
    def trade_resource(self, list_of_resources, returned_resource):
        return False
    
# BOARD BASED CLASSES
class Resource_Hex:
    def __init__(self, points, resource, dice_score):
        self.points = points
        self.resource = resource
        self.dice_score = dice_score

    def __repr__(self):
        return self.resource + ' - ' +  str(self.dice_score)
    

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
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()],
            [(),(),(),(),(),()]
        ]
        return all_combinations

    def random_resource(self, dict_of_resources):
        resource_names = dict_of_resources.keys()
        rand_resource_key = resource_names[random.randint(0, len(dict_of_resources) - 1)]

        dict_of_resources[rand_resource_key] = dict_of_resources[rand_resource_key] - 1
        if dict_of_resources[rand_resource_key] == 0:
            del dict_of_resources[rand_resource_key]
        return rand_resource_key, dict_of_resources

    def randomize_hexes(self):
        resource_types = {'Wood':4, 'Brick':3, 'Sheep':4, 'Wheat':4, 'Stone':3, 'Desert':1}
        dice_list = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        list_of_hexes = []
        for i in range(19): #standard size of board
            points = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
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
                    if not self.check_in_eight(point1, point2):
                        raise Exception('Points aren\'t near each other.') # Points aren't near each other
                else:
                    raise Exception('Second Point isn\'t valid.') # Second Point isn't valid
            else:
                raise Exception('First Point isn\'t valid.') # First Point isn't valid
            
            # CHECK ROAD IS PLAYER ALLOWED
            player = self.players[obj.color]
            player_roads = player.roads

            for player_road in player_roads:
                player_road_p1 = player_road.points[0]
                player_road_p2 = player_road.points[1]
                obj_road_p1 = obj.points[0]
                obj_road_p2 = obj.points[1]

                if player_road_p1 == obj_road_p1:
                    important_point = obj_road_p1
                    if (self.check_houses_for_roads(important_point, player.color)):
                        return True
                elif player_road_p1 == obj_road_p2:
                    important_point = obj_road_p2
                    if (self.check_houses_for_roads(important_point, player.color)):
                        return True
                elif player_road_p2 == obj_road_p1:
                    important_point = obj_road_p1
                    if (self.check_houses_for_roads(important_point, player.color)):
                        return True
                elif player_road_p2 == obj_road_p2:
                    important_point = obj_road_p2
                    if (self.check_houses_for_roads(important_point, player.color)):
                        return True
            raise Exception('You don\'t have a connecting road.')
       
       
        elif isinstance(obj, House):
            # CHECK HOUSE ISN'T TAKEN
            for house in self.houses:
                if house.point == obj.point:
                    return False
            return True
        else:
            return False
        
    def player_buys_road(self, color, road):
        player = self.players[color]
        try:
            if player.buy_road(self.check_availability(road), road.points):
                self.roads.append(road)
            print('bought road')
        except Exception as e:
            print(e)