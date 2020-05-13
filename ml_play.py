"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from mlgame.communication import ml as comm
import random

def ml_loop(side: str):
    """
    The main loop for the machine learning process
    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```
    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False

    blocker_record = 0

    def move_to(player, pred) : #move platform to predicted position to catch ball 
        if player == '1P':
            if scene_info["platform_1P"][0]+25 >= pred and scene_info["platform_1P"][0]+15 <= pred: return 0 # NONE
            elif scene_info["platform_1P"][0]+25 < pred : return 1 # goes right
            else : return 2 # goes left
        else :
            if scene_info["platform_2P"][0]+20 == pred: return 0 # NONE
            elif scene_info["platform_2P"][0]+20 < pred : return 1 # goes right
            else : return 2 # goes left

    def ml_loop_for_1P(): 
        ball_x = scene_info["ball"][0]
        ball_y = scene_info["ball"][1]
        ball_speed_x = scene_info["ball_speed"][0]
        ball_speed_y = scene_info["ball_speed"][1]
        if ball_y > 260 : #下半部
            if ball_speed_y > 0:#求向下
                x = ((415 - ball_y) // ball_speed_y) +1 # 幾個frame以後會需要接  # x means how many frames before catch the ball
                pred = ball_x+(ball_speed_x*x)  # 預測最終位置 # pred means predict ball landing site 
                while True:
                    if pred > 195:
                        pred = 390 - pred
                    elif pred < 0:
                        pred = (-pred)
                    else:
                        break
            else:#球向上
                x = ((ball_y - 260) // (-ball_speed_y)) + 1 + (155//(-ball_speed_y)) + 1
                pred = ball_x+(ball_speed_x*x)  # 預測最終位置 # pred means predict ball landing site 
                while True:
                    if pred > 195:
                        pred = 390 - pred
                    elif pred < 0:
                        pred = (-pred)
                    else:
                        break
        else:
            if ball_speed_y<0:#ball going on
                t1 = ((ball_y-80)//(-ball_speed_y))+((155)//(-ball_speed_y))
                t2 = ((ball_y-80)//(-ball_speed_y))+((180)//(-ball_speed_y))
                if ((ball_y - 80) % ball_speed_y != 0):
                    t1 = t1 + 1
                    t2 = t2 + 1
                if 180 % ball_speed_y != 0:
                    t1 = t1 + 1
                y1 = 80 + ((155)//(-ball_speed_y)) *(-ball_speed_y)
                y2 = 80 + ((180)//(-ball_speed_y))*(-ball_speed_y)
                if 180 % ball_speed_y != 0:
                    y2 = y2 - ball_speed_y
                x1 = ball_x+(ball_speed_x*t1)
                x2 = ball_x+(ball_speed_x*t2)
                while True:
                    if x1 > 195:
                        x1 = 390 - x1
                    elif x1 < 0:
                        x1 = (-x1)
                    else:
                        break
                while True:
                    if x2 > 195:
                        x2 = 390 - x2
                    elif x2 < 0:
                        x2 = (-x2)
                    else:
                        break
                b_speed = scene_info["blocker"][0] - blocker_record
                b1 = scene_info["blocker"][0] + b_speed*t1
                b2 = scene_info["blocker"][0] + b_speed*t2
                minB = 200
                maxB = 0
                if b1 > 170:
                    b1 = 240 - b1
                    maxB = 200
                elif b1 < 0:
                    b1 = (-b1)
                    minB = 0
                if b2 > 170:
                    b2 = 240 - b2
                    maxB = 200
                elif b2 < 0:
                    b2 = (-b2)
                    minB = 0
                if maxB != 200:
                    maxB = max(b1, b2) + 30
                if minB != 0:
                    minB = min(b1, b2)
                
                if x2 > minB and minB > x1:
                    x = ((415-((y1 + y2) / 2))//(-ball_speed_y))+1
                    pred = ((x2 + x1) / 2) + x*(-(abs(ball_speed_x)))
                elif x1 > maxB and maxB > x2:
                    x = ((415-((y1 + y2) / 2))//(-ball_speed_y))+1
                    pred = ((x2 + x1) / 2) + x*(abs(ball_speed_x))
                else:
                    x = (335//(-ball_speed_y))+((ball_y - 80)//(-ball_speed_y))+1
                    pred = ball_x+(ball_speed_x*x)
                while True:
                    if pred > 195:
                        pred = 390 - pred
                    elif pred < 0:
                        pred = (-pred)
                    else:
                        break
            else:
                t1 = (235 - ball_y)//ball_speed_y
                t2 = (260 - ball_y)//ball_speed_y
                if ((260 - ball_y) % ball_speed_y != 0):
                    t2 = t2 + 1
                y1 = ball_y +(ball_speed_y*t1)
                y2 = ball_y +(ball_speed_y*t2)
                if ((260 - ball_y) % ball_speed_y != 0):
                    y2 = y2 + ball_speed_y
                x1 = ball_x+(ball_speed_x*t1)
                x2 = ball_x+(ball_speed_x*t2)
                while True:
                    if x1 > 195:
                        x1 = 390 - x1
                    elif x1 < 0:
                        x1 = (-x1)
                    else:
                        break
                while True:
                    if x2 > 195:
                        x2 = 390 - x2
                    elif x2 < 0:
                        x2 = (-x2)
                    else:
                        break
                b_speed = scene_info["blocker"][0] - blocker_record
                b1 = scene_info["blocker"][0] + b_speed*t1
                b2 = scene_info["blocker"][0] + b_speed*t2
                minB = 200
                maxB = 0
                if b1 > 170:
                    b1 = 240 - b1
                    maxB = 200
                elif b1 < 0:
                    b1 = (-b1)
                    minB = 0
                if b2 > 170:
                    b2 = 240 - b2
                    maxB = 200
                elif b2 < 0:
                    b2 = (-b2)
                    minB = 0
                if maxB != 200:
                    maxB = max(b1, b2) + 30
                if minB != 0:
                    minB = min(b1, b2)
                if x2 > minB and minB > x1:
                    x = ((415-((y1+y2)/2))//ball_speed_y)+1
                    pred = ((x2 + x1) / 2) + x*(-(abs(ball_speed_x)))
                elif x1 > maxB and maxB > x2:
                    x = ((415-((y1+y2)/2))//ball_speed_y)+1
                    pred = ((x2 + x1) / 2) + x*(abs(ball_speed_x))
                else:
                    x = ((415 - ball_y)//ball_speed_y) + 1
                    pred = ball_x+(ball_speed_x*x)
                while True:
                    if pred > 195:
                        pred = 390 - pred
                    elif pred < 0:
                        pred = (-pred)
                    else:
                        break
        return move_to(player = '1P',pred = pred)




    def ml_loop_for_2P():  # as same as 1P
        ball_x = scene_info["ball"][0]
        ball_y = scene_info["ball"][1]
        ball_speed_x = scene_info["ball_speed"][0]
        ball_speed_y = scene_info["ball_speed"][1]
        if scene_info["ball_speed"][1] > 0 : 
            x = ((418 - ball_y) // ball_speed_y) + (335 // ball_speed_y) + 2
            pred = ball_x+(ball_speed_x*x)
            while True:
                if pred > 198:
                    pred = 396 - pred
                elif pred < 3:
                    pred = 6 - pred
                else:
                    break
            return move_to(player = '2P',pred = pred)
        else : 
            x = ((ball_y - 83) // (-ball_speed_y)) + 1
            pred = ball_x+(ball_speed_x*x) 
            while True:
                if pred > 198:
                    pred = 396 - pred
                elif pred < 3:
                    pred = 6 - pred
                else:
                    break
            return move_to(player = '2P',pred = pred)

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information
        

        # 3.4 Send the instruction for this frame to the game process
        blocker_record = scene_info["blocker"][0]
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
        else:
            
            if side == "1P":
                command = ml_loop_for_1P()
            else:
                command = ml_loop_for_2P()

            if command == 0:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif command == 1:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})