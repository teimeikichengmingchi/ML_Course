class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = ()
        self.next_coin = ()
        self.coin_num = 0
        self.computer_cars = []
        self.other_players = []
        self.coins_pos = []
        self.pos_1 = {}
        self.pos_2 = {}
        self.pos_3 = {}
        self.pos_4 = {}
        self.returnArr = []
        print("Initial ml script")

    def find_coin(self):
        pick_this_coin = False
        removed = False
        self.next_coin = ()
        self.coins_pos.sort(key = lambda coin : coin[1])
        for coin in self.coins_pos:
            removed = False
            if self.car_pos[1] - coin[1] < 80:
                for com_car in self.computer_cars:
                    if coin[1] - com_car[1] < 50 and coin[1] - com_car[1] > 10 and abs(coin[0] - com_car[0]) < 40 \
                        and abs(self.car_pos[0] - coin[0]) - 25 < 15 and abs(self.car_pos[1] - coin[1]) - 45 < 20:
                        #if self.player_no == 0:
                            #print(coin, " : removed   0")
                        self.coins_pos.remove(coin)
                        removed = True
                        break
                if removed:
                    continue
            if abs(self.car_pos[0] - coin[0]) > 140 and (self.car_pos[1] - coin[1] + 45) > 0 \
                 and abs(self.car_pos[0] - coin[0] - 25) / (self.car_pos[1] - coin[1] + 45) > (65 / 100): # > (2 / 10)
                #if self.player_no == 0:
                    #print(coin, " : removed   1")
                self.coins_pos.remove(coin)
                removed = True
            if removed:
                continue
            for player_car in self.other_players:
                if (coin[0] > player_car[0] and player_car[0] > self.car_pos[0] and (player_car[1] - self.car_pos[1] < 82)) or \
                     (coin[0] < player_car[0] and player_car[0] < self.car_pos[0] and (player_car[1] - self.car_pos[1] < 82)) or \
                     (abs(coin[0] - player_car[0]) < 15 and (player_car[1] - self.car_pos[1] < 82)):
                    #if self.player_no == 0:
                        #print(coin, " : removed   2")
                    removed = True
                    self.coins_pos.remove(coin)
                    break
        
        for coin in self.coins_pos:
            if coin[1] < self.car_pos[1] + 60:
                pick_this_coin = True
                for car in self.other_players:
                    if abs(car[0] - coin[0]) - 25 < abs(self.car_pos[0] - coin[0]) - 30 and abs(car[1] - coin[1]) - 45 < abs(self.car_pos[1] - coin[1]) - 55 \
                        and abs(car[0] - coin[0]) - 25 < 15 and abs(car[1] - coin[1]) - 45 < 20:
                        pick_this_coin = False
                        break
                """
                if not(self.next_coin == ()):
                    if abs(coin[0] - self.car_pos[0]) - abs(self.next_coin[0] - self.car_pos[0]) > 150:
                        pick_this_coin = False
                """
                if pick_this_coin:
                    self.next_coin = coin
    
    def look_around(self, scene_info: dict):
        """
                self.pos_2     self.pos_4

        self.pos_1        mycar        self.pos_3

        """
        self.pos_1 = {}
        self.pos_2 = {}
        self.pos_3 = {}
        self.pos_4 = {}
        temp = []
        for car in scene_info["cars_info"]:
            if abs(car["pos"][0] - self.car_pos[0]) < 45 and\
                car["pos"][1] < self.car_pos[1] - 77 and car["id"] != self.player_no:
                temp.append(car)
        if len(temp) != 0:
            maxY2 = -999
            maxY4 = -999
            for car in temp:
                if car["pos"][1] > maxY2 and car["pos"][0] <= self.car_pos[0]:
                    maxY2 = car["pos"][1]
                elif car["pos"][1] > maxY4 and car["pos"][0] > self.car_pos[0]:
                    maxY4 = car["pos"][1]
            for car in temp:
                if car["pos"][1] == maxY2:
                    self.pos_2.update(car)
                elif car["pos"][1] == maxY4:
                    self.pos_4.update(car)
        temp = []
        for car in scene_info["cars_info"]:
            if car["pos"][0] - self.car_pos[0] >= 40 and car["pos"][0] - self.car_pos[0] < 80 and car["id"] != self.player_no:
                if self.car_pos[1] >= (car["pos"][1] - 77) and car["pos"][1] >= self.car_pos[1] - 83:
                    temp.append(car)
                    if int(self.car_vel - car["velocity"]) > 0 and (self.car_pos[1] - car["pos"][1] - 83) > 0 and \
                        ((self.car_pos[1] - car["pos"][1] - 83) / int(self.car_vel - car["velocity"])) * 3 > car["pos"][0] - self.car_pos[0] + 45:
                        temp.remove(car)
                    elif self.car_vel - car["velocity"] <= 0 and self.car_pos[1] - car["pos"][1] > 85:
                        temp.remove(car)
        if len(temp) != 0:
            maxY = -999
            for car in temp:
                if car["pos"][1] > maxY:
                    maxY = car["pos"][1]
            for car in temp:
                if car["pos"][1] == maxY:
                    self.pos_3.update(car)
                    break
        temp = []
        for car in scene_info["cars_info"]:
            if self.car_pos[0] - car["pos"][0] >= 40 and self.car_pos[0] - car["pos"][0] < 80 and car["id"] != self.player_no:
                if self.car_pos[1] >= (car["pos"][1] - 77) and car["pos"][1] >= self.car_pos[1] - 83:
                    temp.append(car)
                    if int(self.car_vel - car["velocity"]) > 0 and (self.car_pos[1] - car["pos"][1] - 83) > 0 and \
                        ((self.car_pos[1] - car["pos"][1] - 83) / int(self.car_vel - car["velocity"])) * 3 > self.car_pos[0] - car["pos"][0] + 45:
                        temp.remove(car)
                    elif self.car_vel - car["velocity"] <= 0 and self.car_pos[1] - car["pos"][1] > 85:
                        temp.remove(car)
        if len(temp) != 0:
            maxY = -999
            for car in temp:
                if car["pos"][1] > maxY:
                    maxY = car["pos"][1]
            for car in temp:
                if car["pos"][1] == maxY:
                    self.pos_1.update(car)
                    break
    
    def move_y(self, dest : tuple, speed : int):
        if "SPEED" in self.returnArr:
            self.returnArr.remove("SPEED")
        if dest[1] - self.car_pos[1] > 0 and speed > 0 and (dest[1] - self.car_pos[1] / speed) > 20:
            self.returnArr.append("BRAKE")
        elif dest[1] - self.car_pos[1] > 0 and speed <= 0:
            self.returnArr.append("BRAKE")
        elif dest[1] < self.car_pos[1] < dest[1] + 10:
            self.returnArr.append("SPEED")
        elif dest[1] - self.car_pos[1] < 0 and speed <= 0:
            self.returnArr.append("SPEED")
        elif dest[1] - self.car_pos[1] < 0 and speed > 0 and (-(dest[1] - self.car_pos[1]) / speed) * 3 > dest[0]:
            self.returnArr.append("SPEED")
        elif dest[1] - self.car_pos[1] < 0 and speed > 0 and (-(dest[1] - self.car_pos[1]) / speed) * 3 < dest[0]:
            pass
        
    
    def move_right(self):
        self.returnArr.append("MOVE_RIGHT")
        if self.pos_3 != {}:
            if self.next_coin != () and self.next_coin[1] > self.pos_3["pos"][1] + 45:
                if self.car_pos[1] > self.pos_3["pos"][1] :
                    self.move_y((1000, self.pos_3["pos"][1] + 90), int(self.pos_3["velocity"] - self.car_vel))
                    if self.pos_3["pos"][0] - self.car_pos[0] - 40 < 10:
                        self.returnArr.remove("MOVE_RIGHT")
                    elif self.pos_3["pos"][0] - self.car_pos[0] - 40 <= 6:
                        self.returnArr.append("MOVE_LEFT")
                    if self.car_pos[1] - self.pos_3["pos"][1] > 85:
                        self.returnArr.append("MOVE_RIGHT")
            elif self.pos_4 != {}:#both of pos4 and pos3 are occupied
                if self.pos_3["pos"][1] - self.pos_4["pos"][1] - 80 - ((self.pos_3["pos"][0] - self.car_pos[0]) / 3) * int(self.pos_3["velocity"] - self.pos_4["velocity"]) > 60:# 從pos3上面過
                    self.move_y((self.pos_3["pos"][0], self.pos_4["pos"][1] + 90), int(self.car_vel - self.pos_4["velocity"]))
                    if self.pos_3["pos"][0] - self.car_pos[0] - 40 < 10:
                        self.returnArr.remove("MOVE_RIGHT")
                    elif self.pos_3["pos"][0] - self.car_pos[0] - 40 <= 6:
                        self.returnArr.append("MOVE_LEFT")
                else:#從pos3下面過
                    self.move_y((self.pos_3["pos"][0], self.pos_3["pos"][1] + 90), int(self.pos_3["velocity"] - self.car_vel))
                    if self.pos_3["pos"][0] - self.car_pos[0] - 40 < 10:
                        self.returnArr.remove("MOVE_RIGHT")
                    elif self.pos_3["pos"][0] - self.car_pos[0] - 40 <= 6:
                        self.returnArr.append("MOVE_LEFT")
                    if self.car_pos[1] - self.pos_3["pos"][1] > 85:
                        self.returnArr.append("MOVE_RIGHT")
            elif self.pos_2 != {}:#both of pos2 and pos3 are occupied，四不在
                if self.pos_3["pos"][1] - self.pos_2["pos"][1] - 80 - ((self.pos_3["pos"][0] - self.car_pos[0]) / 3) * int(self.pos_3["velocity"] - self.pos_2["velocity"]) > 60:# 從pos3上面過
                    self.move_y((self.pos_3["pos"][0], self.pos_2["pos"][1] + 90), int(self.car_vel - self.pos_2["velocity"]))
                    if self.pos_3["pos"][0] - self.car_pos[0] - 40 < 10:
                        self.returnArr.remove("MOVE_RIGHT")
                    elif self.pos_3["pos"][0] - self.car_pos[0] - 40 <= 6:
                        self.returnArr.append("MOVE_LEFT")
                else:#從pos3下面過
                    self.move_y((self.pos_3["pos"][0], self.pos_3["pos"][1] + 90), int(self.pos_3["velocity"] - self.car_vel))
                    if self.pos_3["pos"][0] - self.car_pos[0] - 40 < 10:
                        self.returnArr.remove("MOVE_RIGHT")
                    elif self.pos_3["pos"][0] - self.car_pos[0] - 40 <= 6:
                        self.returnArr.append("MOVE_LEFT")
                    if self.car_pos[1] - self.pos_3["pos"][1] > 85:
                        self.returnArr.append("MOVE_RIGHT")
            else:# 從pos3上面過
                self.move_y((self.pos_3["pos"][0], self.pos_3["pos"][1] - 1000), 0)
                if self.pos_3["pos"][0] - self.car_pos[0] - 40 < 10:
                        self.returnArr.remove("MOVE_RIGHT")
                elif self.pos_3["pos"][0] - self.car_pos[0] - 40 <= 6:
                    self.returnArr.append("MOVE_LEFT")
        else:
            if self.pos_4 != {} and self.pos_2 != {}:
                if self.pos_4["pos"][1] > self.pos_2["pos"][1]:
                    self.move_y((1000, self.pos_4["pos"][1] + 90), int(self.car_vel - self.pos_4["velocity"]))
                else:
                    self.move_y((1000, self.pos_2["pos"][1] + 90), int(self.car_vel - self.pos_2["velocity"]))
            elif self.pos_4 != {}:
                self.move_y((1000, self.pos_4["pos"][1] + 90), int(self.car_vel - self.pos_4["velocity"]))
            elif self.pos_2 != {}:
                self.move_y((1000, self.pos_2["pos"][1] + 90), int(self.car_vel - self.pos_2["velocity"]))
            else:
                self.move_y((1000, 0), 0)
    
    def move_left(self):
        self.returnArr.append("MOVE_LEFT")
        if self.pos_1 != {}:
            if self.next_coin != () and self.next_coin[1] > self.pos_1["pos"][1] + 45:
                if self.car_pos[1] > self.pos_1["pos"][1]:
                    self.move_y((-1000, self.pos_1["pos"][1] + 90), int(self.pos_1["velocity"] - self.car_vel))
                    if self.car_pos[0] - self.pos_1["pos"][0] - 40 < 10:
                        self.returnArr.remove("MOVE_LEFT")
                    elif self.car_pos[0] - self.pos_1["pos"][0] - 40 <= 6:
                        self.returnArr.append("MOVE_RIGHT")
                    if self.car_pos[1] - self.pos_1["pos"][1] > 85:
                        self.returnArr.append("MOVE_LEFT")
            elif self.pos_4 != {}:#both of pos4 and pos1 are occupied
                if self.pos_1["pos"][1] - self.pos_4["pos"][1] - 80 - ((self.pos_1["pos"][0] - self.car_pos[0]) / 3) * int(self.pos_1["velocity"] - self.pos_4["velocity"]) > 60:# 從pos1上面過
                    self.move_y((self.pos_1["pos"][0], self.pos_4["pos"][1] + 90), int(self.car_vel - self.pos_4["velocity"]))
                    if self.car_pos[0] - self.pos_1["pos"][0] - 40 < 10:
                        self.returnArr.remove("MOVE_LEFT")
                    elif self.car_pos[0] - self.pos_1["pos"][0] - 40 <= 6:
                        self.returnArr.append("MOVE_RIGHT")
                else:#從pos1下面過
                    self.move_y((self.pos_1["pos"][0], self.pos_1["pos"][1] + 90), int(self.pos_1["velocity"] - self.car_vel))
                    if self.car_pos[0] - self.pos_1["pos"][0] - 40 < 10:
                        self.returnArr.remove("MOVE_LEFT")
                    elif self.car_pos[0] - self.pos_1["pos"][0] - 40 <= 6:
                        self.returnArr.append("MOVE_RIGHT")
                    if self.car_pos[1] - self.pos_1["pos"][1] > 85:
                        self.returnArr.append("MOVE_LEFT")
            elif self.pos_2 != {}:#both of pos2 and pos3 are occupied，四不在
                if self.pos_1["pos"][1] - self.pos_2["pos"][1] - 80 - ((self.pos_1["pos"][0] - self.car_pos[0]) / 3) * int(self.pos_1["velocity"] - self.pos_2["velocity"]) > 60:# 從pos3上面過
                    self.move_y((self.pos_1["pos"][0], self.pos_2["pos"][1] + 90), int(self.car_vel - self.pos_2["velocity"]))
                    if self.car_pos[0] - self.pos_1["pos"][0] - 40 < 10:
                        self.returnArr.remove("MOVE_LEFT")
                    elif self.car_pos[0] - self.pos_1["pos"][0] - 40 <= 6:
                        self.returnArr.append("MOVE_RIGHT")
                else:#從pos3下面過
                    self.move_y((self.pos_1["pos"][0], self.pos_1["pos"][1] + 90), int(self.pos_1["velocity"] - self.car_vel))
                    if self.car_pos[0] - self.pos_1["pos"][0] - 40 < 10:
                        self.returnArr.remove("MOVE_LEFT")
                    elif self.car_pos[0] - self.pos_1["pos"][0] - 40 <= 6:
                        self.returnArr.append("MOVE_RIGHT")
                    if self.car_pos[1] - self.pos_1["pos"][1] > 85:
                        self.returnArr.append("MOVE_LEFT")
            else:# 從pos3上面過
                self.move_y((self.pos_1["pos"][0], self.pos_1["pos"][1] - 1000), 0)
                if self.car_pos[0] - self.pos_1["pos"][0] - 40 < 10:
                    self.returnArr.remove("MOVE_LEFT")
                elif self.car_pos[0] - self.pos_1["pos"][0] - 40 <= 6:
                    self.returnArr.append("MOVE_RIGHT")
        else:
            if self.pos_4 != {} and self.pos_2 != {}:
                if self.pos_4["pos"][1] > self.pos_2["pos"][1]:
                    self.move_y((-1000, self.pos_4["pos"][1] + 90), int(self.car_vel - self.pos_4["velocity"]))
                else:
                    self.move_y((-1000, self.pos_2["pos"][1] + 90), int(self.car_vel - self.pos_2["velocity"]))
            elif self.pos_4 != {}:
                self.move_y((-1000, self.pos_4["pos"][1] + 90), int(self.car_vel - self.pos_4["velocity"]))
            elif self.pos_2 != {}:
                self.move_y((-1000, self.pos_2["pos"][1] + 90), int(self.car_vel - self.pos_2["velocity"]))
            else:
                self.move_y((-1000, 0), 0)
    
    
    def move(self):
        self.returnArr = []
        self.returnArr.append("SPEED")
        if self.next_coin != ():
            if self.next_coin[0] > self.car_pos[0] + 15:
                self.move_right()
            elif self.next_coin[0] < self.car_pos[0] - 15:
                self.move_left()
        if not("MOVE_LEFT" in self.returnArr or "MOVE_RIGHT" in self.returnArr):#繞路還沒寫完
            if self.pos_2 != {} and self.pos_4 == {} and self.car_pos[1] - self.pos_2["pos"][1] - 80 < 120:
                self.move_right()
            elif self.pos_4 != {} and self.pos_2 == {} and self.car_pos[1] - self.pos_4["pos"][1] - 80 < 120:
                self.move_left()
            elif self.pos_2 != {} and self.pos_4 != {}:
                if self.car_pos[1] - self.pos_2["pos"][1] - 80 < 120:
                    if self.car_pos[1] - self.pos_4["pos"][1] - 80 > 200:
                        self.move_right()
                    else:
                        self.move_left()
                elif self.car_pos[1] - self.pos_4["pos"][1] - 80 < 120:
                    if self.car_pos[1] - self.pos_2["pos"][1] - 80 > 200:
                        self.move_left()
                    else:
                        self.move_right()
    """
    def move(self):
        self.returnArr = []
        self.returnArr.append("SPEED")
        if self.next_coin != ():
            if self.next_coin[0] > self.car_pos[0] + 15:
                self.returnArr.append("MOVE_RIGHT")
            elif self.next_coin[0] < self.car_pos[0] - 15:
                self.returnArr.append("MOVE_LEFT")
        if "MOVE_RIGHT" in self.returnArr and self.pos_3 != {} and self.pos_3["pos"][0] - self.car_pos[0] - 40 < 10:
            self.returnArr.remove("MOVE_RIGHT")
        elif "MOVE_LEFT" in self.returnArr and self.pos_1 != {} and self.car_pos[0] - self.pos_1["pos"][0] - 40 < 10:
            self.returnArr.remove("MOVE_LEFT")
        if self.pos_3 != {} and self.pos_3["pos"][0] - self.car_pos[0] - 40 <= 6:
            self.returnArr.append("MOVE_LEFT")
        elif self.pos_1 != {} and self.car_pos[0] - self.pos_1["pos"][0] - 40 <= 6:
            self.returnArr.append("MOVE_RIGHT")
    """

    def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "ALIVE":
            return "RESET"
        
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]
            self.other_players = []
            for car in scene_info["cars_info"]:
                if car["id"] == self.player_no:
                    self.car_vel = car["velocity"]
                    self.coin_num = car["coin_num"]
                elif car["id"] < 100:
                    self.other_players.append(car["pos"])
            self.computer_cars = scene_info["computer_cars"]
            if scene_info.__contains__("coins"):
                self.coins_pos = scene_info["coins"]
            self.find_coin()
            self.look_around(scene_info)
            self.move()

        
        if self.car_vel >= 0:
            if self.player_no == 0:
                print(self.player, " ", self.car_pos, " ", scene_info["frame"], "\npos1 = ", self.pos_1, "pos2 = ", self.pos_2, "pos4 = ", self.pos_4, "pos3 = ", self.pos_3)
                #print(self.other_players)
                #print("pos1 = ", self.pos_1, "pos2 = ", self.pos_2, "pos4 = ", self.pos_4, "pos3 = ", self.pos_3)
                #print(self.player, " : ", self.next_coin, " ", scene_info["frame"])
        
        return self.returnArr

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
